from django.conf import settings
from django.db import models
from django_fsm.db.fields import FSMField, transition
from django_gocardless.client import get_client, get_merchant_client
from django_gocardless.partners.models import PartnerMerchant
from django_gocardless.returntrips.models import ReturnTrippableMixin
from django_gocardless.utils import logger
from django_gocardless.bills import signals


class Bill(ReturnTrippableMixin, models.Model):
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    STATUS_CHOICES = (
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bills_sent')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bills_received', default=None, null=True)
    return_trip = models.ForeignKey('returntrips.ReturnTrip', default=None, null=True)
    amount  = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    user_company_name = models.CharField(max_length=200, default=None, null=True)
    user_postal_code = models.CharField(max_length=16, default=None, null=True)
    status = FSMField(default=INACTIVE, choices=STATUS_CHOICES)

    resource_uri = models.CharField(max_length=255, default='', blank=True)
    resource_id = models.CharField(max_length=255, default='', blank=True, db_index=True)
    resource_type = 'bill'

    def get_client(self):
        if self.to_user:
            merchant = PartnerMerchant.objects.filter(user=self.to_user, status=PartnerMerchant.AVAILABLE)
            if not len(merchant):
                raise Exception('No merchant for user %s with status available' % self.to_user)
            else:
                client = get_merchant_client(merchant[0].merchant_id)
        else:
            client = get_client()

        return client

    def make_departure_uri(self, redirect_uri, cancel_uri, state):
        user_details = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'company_name': self.user_company_name,
            'email': self.user.email,
            'postal_code': self.user_postal_code,
        }
        return self.get_client().new_bill_url(
            amount=self.amount,
            name=self.name,
            description=self.description,
            user=user_details,
            redirect_uri=redirect_uri,
            cancel_uri=cancel_uri,
            state=state,
        )

    @transition(status, source=INACTIVE, target=ACTIVE)
    def user_returns(self, request, payload, return_trip):
        try:
            get_client().confirm_resource(payload)
        except:
            logger.exception('Failed to confirm bill')
            raise

        self.resource_uri = payload['resource_uri']
        self.resource_id = payload['resource_id']

        signals.bill_paid.send(Bill, bill=self, request=request)


