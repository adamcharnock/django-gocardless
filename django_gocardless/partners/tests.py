from mock import patch
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_gocardless.client import get_client
from django_gocardless.partners.models import PartnerMerchant
from django_gocardless.returntrips.models import ReturnTrip

OK_URL = 'https://sandbox.gocardless.com/oauth/authorize?client_id=abcdefghijlmnopqrstuvwxyzabcdefghijlmnopqrstuvwxyz&merchant%5Bname%5D=&merchant%5Buser%5D%5Bemail%5D=a%40a.com&redirect_uri=https%3A%2F%2Fexample.com%2Fredirect-return%2F&response_type=code&scope=manage_merchant&state=1'
RETURN_QS = '?code=DH8pg5qbz00K3AUQ9UtnJAcvUkIu0TZhO1dhiT4JcUCR%2B7%2BDgK1BwF5uzXiFHvXp&state=3'

class PartnerDepartViewTestCase(TestCase):

    def test_ok(self):
        user = get_user_model().objects.create(username='testuser', email='a@a.com')
        user.set_password('pass')
        user.save()
        self.client.login(username='testuser', password='pass')
        #with patch.object(get_client(), 'confirm_resource', lambda params: True):
        resp = self.client.get(reverse('gocardless_partner_depart'), data={'redirect_uri': 'http://example.com/'})
        self.assertEqual(resp.status_code, 302, resp.content)
        self.assertEqual(resp['Location'], OK_URL)

        return_trip = ReturnTrip.objects.get()
        partner_merchant = PartnerMerchant.objects.get()

        self.assertEqual(return_trip.for_model_class, 'partners.PartnerMerchant')
        self.assertEqual(return_trip.for_pk, partner_merchant.pk)
        self.assertEqual(return_trip.status, 'departed')
        self.assertEqual(return_trip.success_uri, 'http://example.com/')
        self.assertEqual(return_trip.cancel_uri, 'http://example.com/')
        self.assertEqual(return_trip.is_signed, False)

        self.assertEqual(partner_merchant.user, user)
        self.assertEqual(partner_merchant.return_trip, return_trip)
        self.assertEqual(partner_merchant.authorization_code, None)
        self.assertEqual(partner_merchant.access_token, None)
        self.assertEqual(partner_merchant.token_type, None)
        self.assertEqual(partner_merchant.scope, None)
        self.assertEqual(partner_merchant.merchant_id, None)
        self.assertEqual(partner_merchant.status, PartnerMerchant.PENDING)

    def test_return(self):
        user = get_user_model().objects.create(username='testuser', email='a@a.com')
        user.set_password('pass')
        user.save()

        return_trip = ReturnTrip.objects.create(
            pk=3,
            for_model_class='partners.PartnerMerchant',
            for_pk=1,
            success_uri='http://example.com/',
            cancel_uri='http://example.com/',
            is_signed=False,
            extra_state='some-extra-state'
        )
        partner_merchant = PartnerMerchant.objects.create(
            pk=1,
            user=user,
            return_trip=return_trip,
            status=PartnerMerchant.PENDING,
        )

        self.client.login(username='testuser', password='pass')
        with patch.object(get_client(), '_request', lambda *args, **kwargs: {'access_token': 'accesstoken123', 'scope': 'manage_merchant:merchantid123'}):
            resp = self.client.get(reverse('gocardless_redirect_return') + RETURN_QS)
        self.assertEqual(resp.status_code, 302, resp.content)
        self.assertEqual(resp['Location'], 'http://example.com/?state=some-extra-state')

        partner_merchant = PartnerMerchant.objects.get()
        self.assertEqual(partner_merchant.pk, 1)
        self.assertEqual(partner_merchant.access_token, 'accesstoken123')
        self.assertEqual(partner_merchant.merchant_id, 'merchantid123')
        self.assertEqual(partner_merchant.scope, 'manage_merchant')
        self.assertEqual(partner_merchant.authorization_code, 'DH8pg5qbz00K3AUQ9UtnJAcvUkIu0TZhO1dhiT4JcUCR+7+DgK1BwF5uzXiFHvXp')
        self.assertEqual(partner_merchant.token_type, 'bearer')
        self.assertEqual(partner_merchant.user, user)
        self.assertEqual(partner_merchant.status, PartnerMerchant.AVAILABLE)

