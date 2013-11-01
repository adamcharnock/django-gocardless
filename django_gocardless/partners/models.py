from django.conf import settings
from django.db import models
from django_fsm.db.fields import FSMField, transition
from django_gocardless.client import get_client
from django_gocardless.returntrips.models import ReturnTrippableMixin


class PartnerMerchant(ReturnTrippableMixin, models.Model):
    PENDING = 'pending'
    AVAILABLE = 'available'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (AVAILABLE, 'Available'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='partner_merchants')
    return_trip = models.ForeignKey('returntrips.ReturnTrip', default=None, null=True)
    authorization_code = models.CharField(max_length=200, default=None, null=True)
    access_token = models.CharField(max_length=200, default=None, null=True)
    token_type = models.CharField(max_length=200, default=None, null=True)
    scope = models.CharField(max_length=200, default=None, null=True)
    merchant_id = models.CharField(max_length=200, default=None, null=True)
    status = FSMField(default=PENDING, choices=STATUS_CHOICES)

    def exchange_code(self):
        client = get_client()
        client.fetch_access_token(self.return_trip.internal_redirect_uri, self.authorization_code)
        self.access_token = client._access_token
        self.merchant_id = client._merchant_id
    exchange_code.alters_data = True

    def make_departure_uri(self, redirect_uri, cancel_uri, state):
        merchant_details = {
            'name': self.user.get_full_name(),
            'user': {
                'email': self.user.email,
            }
        }
        # Cancel URI is not an option here
        return get_client().new_merchant_url(
            redirect_uri=redirect_uri,
            merchant=merchant_details,
            state=state,
        )

    @transition(status, source=PENDING, target=AVAILABLE)
    def user_returns(self, request, payload, return_trip):
        self.authorization_code = payload['code']
        self.exchange_code()
        # This information is actually returned form GoCardless,
        # but the python client doesn't give us access to it
        # and it is non-changing anyway.
        self.scope = 'manage_merchant'
        self.token_type = 'bearer'

