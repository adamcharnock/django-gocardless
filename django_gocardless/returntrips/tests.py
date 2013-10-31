from mock import patch
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_gocardless.client import get_client
from django_gocardless.preauthorizations.models import PreAuthorization
from django_gocardless.returntrips.models import ReturnTrip

RETURN_QS_OK = '?resource_id=0FESY5V68N&resource_type=pre_authorization&resource_uri=https%3A%2F%2Fsandbox.gocardless.com%2Fapi%2Fv1%2Fpre_authorizations%2F0FESY5V68N&signature=f0d9b311b4027f91fca7ef4c0ac0d8924d217747df52adb80d8b6279af963eba&state=123456'
RETURN_QS_BAD_SIG = '?resource_id=0FESY5V68N&resource_type=pre_authorization&resource_uri=https%3A%2F%2Fsandbox.gocardless.com%2Fapi%2Fv1%2Fpre_authorizations%2F0FESY5V68N&signature=xxxxxxxxxxxxxxxxxxxxxxx&state=123456'
RETURN_QS_BAD_STATE = '?resource_id=0FESY5V68N&resource_type=pre_authorization&resource_uri=https%3A%2F%2Fsandbox.gocardless.com%2Fapi%2Fv1%2Fpre_authorizations%2F0FESY5V68N&signature=f0d9b311b4027f91fca7ef4c0ac0d8924d217747df52adb80d8b6279af963eba&state=abc'

class ReturnViewTestCase(TestCase):
    def test_ok(self):
        pre_auth = PreAuthorization.objects.create(pk=12, max_amount=100)
        return_trip = ReturnTrip.objects.create(pk=123456, for_model_class='preauthorizations.PreAuthorization', for_pk=12)

        with patch.object(get_client(), 'confirm_resource', lambda params: True):
            resp = self.client.get(reverse('gocardless_redirect_return') + RETURN_QS_OK)
        self.assertEqual(resp.status_code, 302, resp.content)

        return_trip = ReturnTrip.objects.get(pk=123456)
        pre_auth = PreAuthorization.objects.get(pk=12)
        self.assertEqual(return_trip.status, 'returned')
        self.assertEqual(pre_auth.status, 'active')

    def test_bad_sig(self):
        resp = self.client.get(reverse('gocardless_redirect_return') + RETURN_QS_BAD_SIG)
        self.assertEqual(resp.status_code, 400)

    def test_bad_state(self):
        resp = self.client.get(reverse('gocardless_redirect_return') + RETURN_QS_BAD_STATE)
        self.assertEqual(resp.status_code, 400)

    def test_ok_unsigned(self):
        pre_auth = PreAuthorization.objects.create(pk=12, max_amount=100)
        return_trip = ReturnTrip.objects.create(is_signed=False, pk=123456, for_model_class='preauthorizations.PreAuthorization', for_pk=12)

        with patch.object(get_client(), 'confirm_resource', lambda params: True):
            resp = self.client.get(reverse('gocardless_redirect_return') + RETURN_QS_BAD_SIG)
        self.assertEqual(resp.status_code, 302, resp.content)

        return_trip = ReturnTrip.objects.get(pk=123456)
        pre_auth = PreAuthorization.objects.get(pk=12)
        self.assertEqual(return_trip.status, 'returned')
        self.assertEqual(pre_auth.status, 'active')

