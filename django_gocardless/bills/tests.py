from decimal import Decimal
from urlparse import parse_qs
from mock import patch
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_gocardless.bills.models import Bill
from django_gocardless.client import get_client
from django_gocardless.partners.models import PartnerMerchant
from django_gocardless.returntrips.models import ReturnTrip

OK_URL = 'https://sandbox.gocardless.com/connect/bills/new?bill%5Bamount%5D=12.34&bill%5Bdescription%5D=Bill%20description&bill%5Bmerchant_id%5D=123456&bill%5Bname%5D=Test%20Bill&bill%5Buser%5D%5Bcompany_name%5D=Acme%20Ltd&bill%5Buser%5D%5Bemail%5D=a%40a.com&bill%5Buser%5D%5Bfirst_name%5D=&bill%5Buser%5D%5Blast_name%5D=&bill%5Buser%5D%5Bpostal_code%5D=XX1%201XX&client_id=abcdefghijlmnopqrstuvwxyzabcdefghijlmnopqrstuvwxyz&nonce=3pexr4nUgHzP4cZguaqmmyktwXEwt5gP6bPQQ%2FfNPUzAvmKUZrBigA%3D%3D&redirect_uri=https%3A%2F%2Fexample.com%2Fredirect-return%2F&signature=28fd2118fce737d2529dc77a7281794f6b13c2e0262bb99811b524f945c809a1&state=1&timestamp=2013-11-01T13%3A53%3A42Z'
OK_TO_USER_URL = 'https://sandbox.gocardless.com/connect/bills/new?bill%5Bamount%5D=12.34&bill%5Bdescription%5D=Bill%20description&bill%5Bmerchant_id%5D=xyzxyz&bill%5Bname%5D=Test%20Bill&bill%5Buser%5D%5Bcompany_name%5D=Acme%20Ltd&bill%5Buser%5D%5Bemail%5D=a%40a.com&bill%5Buser%5D%5Bfirst_name%5D=&bill%5Buser%5D%5Blast_name%5D=&bill%5Buser%5D%5Bpostal_code%5D=XX1%201XX&client_id=abcdefghijlmnopqrstuvwxyzabcdefghijlmnopqrstuvwxyz&nonce=3pexr4nUgHzP4cZguaqmmyktwXEwt5gP6bPQQ%2FfNPUzAvmKUZrBigA%3D%3D&redirect_uri=https%3A%2F%2Fexample.com%2Fredirect-return%2F&signature=28fd2118fce737d2529dc77a7281794f6b13c2e0262bb99811b524f945c809a1&state=2&timestamp=2013-11-01T13%3A53%3A42Z'
RETURN_QS = '?resource_id=0FPYX3MRCD&resource_type=bill&resource_uri=https%3A%2F%2Fsandbox.gocardless.com%2Fapi%2Fv1%2Fbills%2F0FPYX3MRCD&signature=c9e321da30aa0eb72c1788f6b2d3fe3f22e070cc848c216e70bcf4384e5fdf5e&state=3'

class PartnerDepartViewTestCase(TestCase):

    def assertUrlPathEqual(self, url1, url2):
        url1 = url1.split('?')[0]
        url2 = url1.split('?')[0]
        if url1 != url2:
            raise AssertionError("URL path components do not match: '%s' != '%s'" % (url1, url2))

    def assertQueryStringEqual(self, url1, url2, ignore=None):
        url1 = url1.split('?', 2)
        url2 = url2.split('?', 2)
        qs1 = parse_qs('' if len(url1) == 1 else url1[1])
        qs2 = parse_qs('' if len(url2) == 1 else url2[1])
        for k in ignore or ():
            qs1.pop(k, None)
            qs2.pop(k, None)
        self.assertDictEqual(qs1, qs2)

    def test_ok(self):
        user = get_user_model().objects.create(username='testuser', email='a@a.com')
        user.set_password('pass')
        user.save()
        self.client.login(username='testuser', password='pass')

        resp = self.client.get(reverse('gocardless_bill_depart'), data={
            'redirect_uri': 'http://example.com/',
            'cancel_uri': 'http://example.com/cancel/',
            'state': 'moo',
            'amount': '12.34',
            'name': 'Test Bill',
            'description': 'Bill description',
            'user_company_name': 'Acme Ltd',
            'user_postal_code': 'XX1 1XX',
        })
        self.assertEqual(resp.status_code, 302, resp.content)
        self.assertUrlPathEqual(resp['Location'], OK_URL)
        self.assertQueryStringEqual(resp['Location'], OK_URL, ignore=['nonce', 'timestamp', 'signature'])

        return_trip = ReturnTrip.objects.get()
        bill = Bill.objects.get()

        self.assertEqual(return_trip.for_model_class, 'bills.Bill')
        self.assertEqual(return_trip.for_pk, bill.pk)
        self.assertEqual(return_trip.status, 'departed')
        self.assertEqual(return_trip.extra_state, 'moo')
        self.assertEqual(return_trip.success_uri, 'http://example.com/')
        self.assertEqual(return_trip.cancel_uri, 'http://example.com/cancel/')
        self.assertEqual(return_trip.is_signed, False)

        self.assertEqual(bill.user, user)
        self.assertEqual(bill.return_trip, return_trip)
        self.assertEqual(bill.status, Bill.INACTIVE)
        self.assertEqual(bill.amount, Decimal('12.34'))
        self.assertEqual(bill.name, 'Test Bill')
        self.assertEqual(bill.description, 'Bill description')
        self.assertEqual(bill.user_company_name, 'Acme Ltd')
        self.assertEqual(bill.user_postal_code, 'XX1 1XX')
        self.assertEqual(bill.resource_uri, '')
        self.assertEqual(bill.resource_id, '')

    def test_ok_to_user(self):
        user = get_user_model().objects.create(username='testuser', email='a@a.com')
        user.set_password('pass')
        user.save()
        self.client.login(username='testuser', password='pass')

        to_user = get_user_model().objects.create(username='touser', email='to@user.com')
        pm_return_trip = ReturnTrip.objects.create(
            pk=1,
            for_model_class='partners.PartnerMerchant',
            for_pk=9,
            success_uri='http://example.com/',
            cancel_uri='http://example.com/',
        )
        to_user_partner_merchant = PartnerMerchant.objects.create(
            pk=9,
            user=to_user,
            status=PartnerMerchant.AVAILABLE,
            return_trip=pm_return_trip,
            merchant_id='xyzxyz',
        )

        resp = self.client.get(reverse('gocardless_bill_depart'), data={
            'redirect_uri': 'http://example.com/',
            'cancel_uri': 'http://example.com/cancel/',
            'state': 'moo',
            'amount': '12.34',
            'name': 'Test Bill',
            'description': 'Bill description',
            'user_company_name': 'Acme Ltd',
            'user_postal_code': 'XX1 1XX',
            'to_user': str(to_user.pk),
        })
        self.assertEqual(resp.status_code, 302, resp.content)
        self.assertUrlPathEqual(resp['Location'], OK_TO_USER_URL)
        self.assertQueryStringEqual(resp['Location'], OK_TO_USER_URL, ignore=['nonce', 'timestamp', 'signature'])

        bill = Bill.objects.get()

        self.assertEqual(bill.user, user)
        self.assertEqual(bill.to_user, to_user)

    def test_return(self):
        user = get_user_model().objects.create(username='testuser', email='a@a.com')
        user.set_password('pass')
        user.save()

        return_trip = ReturnTrip.objects.create(
            pk=3,
            for_model_class='bills.Bill',
            for_pk=1,
            success_uri='http://example.com/',
            cancel_uri='http://example.com/',
            is_signed=False,
            extra_state='some-extra-state'
        )
        bill = Bill.objects.create(
            pk=1,
            user=user,
            return_trip=return_trip,
            status=Bill.INACTIVE,
            amount='12.34',
            name='Test Bill',
        )

        self.client.login(username='testuser', password='pass')
        with patch.object(get_client(), 'confirm_resource', lambda *args, **kwargs: True):
            resp = self.client.get(reverse('gocardless_redirect_return') + RETURN_QS)
        self.assertEqual(resp.status_code, 302, resp.content)
        self.assertEqual(resp['Location'], 'http://example.com/?state=some-extra-state')

        bill = Bill.objects.get()
        self.assertEqual(bill.pk, 1)
        self.assertEqual(bill.resource_uri, 'https://sandbox.gocardless.com/api/v1/bills/0FPYX3MRCD')
        self.assertEqual(bill.resource_id, '0FPYX3MRCD')
        self.assertEqual(bill.status, Bill.ACTIVE)

