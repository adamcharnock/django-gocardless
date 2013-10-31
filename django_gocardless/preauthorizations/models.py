import logging
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django_fsm.db.fields import FSMField, transition
from django_gocardless.client import get_client
from django_gocardless.returntrips.models import ReturnTrippableMixin
from django_gocardless.utils import logger
from django_gocardless.webhook import signals

class PreAuthorizationManager(models.Manager):
    def active(self):
        return self.filter(status=PreAuthorization.ACTIVE)
    def cancelled(self):
        return self.filter(status=PreAuthorization.CANCELLED)
    def expired(self):
        return self.filter(status=PreAuthorization.EXPIRED)


class PreAuthorization(ReturnTrippableMixin, models.Model):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'

    INTERVAL_UNIT_CHOICES = (
        (DAY, 'Day'),
        (WEEK, 'Week'),
        (MONTH, 'Month'),
    )

    INACTIVE = 'inactive'
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'
    STATUS_CHOICES = (
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (CANCELLED, 'Cancelled'),
        (EXPIRED, 'Expired'),
    )

    created = models.DateTimeField(auto_now=True)
    status = FSMField(default=INACTIVE, choices=STATUS_CHOICES)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interval_length = models.SmallIntegerField(default=1)
    interval_unit = models.CharField(max_length=10, default=MONTH, choices=INTERVAL_UNIT_CHOICES)
    expires_at = models.DateField(default=None, null=True, blank=True)
    interval_count = models.SmallIntegerField(default=None, blank=True, null=True, help_text='After how many intervals does this pre-auth expire')
    name = models.CharField(max_length=255, blank=True, default='', help_text='Brief description used to identify the pre-authorization, displayed to the user alongside the amount. Often useful for an "invoice reference"')
    description = models.TextField(default='', blank=True, help_text='More verbose description, which will be displayed to the user')
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    calendar_intervals = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='preauthorizations')

    resource_uri = models.CharField(max_length=255, default='', blank=True)
    resource_id = models.CharField(max_length=255, default='', blank=True, db_index=True)
    resource_type = 'pre_authorization'

    objects = PreAuthorizationManager()

    def make_departure_uri(self, redirect_uri, state):
        client = get_client()
        return client.new_pre_authorization_url(
            max_amount=self.max_amount,
            interval_length=self.interval_length,
            interval_unit=self.interval_unit,
            expires_at=self.expires_at,
            name=self.name or None,
            description=self.description or None,
            interval_count=self.interval_count,
            calendar_intervals=self.calendar_intervals,
            redirect_uri=redirect_uri,
            state=state,
        )

    @transition(source=INACTIVE, target=ACTIVE)
    def user_returns(self, request, payload, return_trip):
        # Now confirm
        try:
            get_client().confirm_resource(payload)
        except:
            logger.exception('Failed to confirm resource on return trip')

        self.resource_uri = payload['resource_uri']
        self.resource_id = payload['resource_id']

    @transition(source='*', target=CANCELLED)
    def cancel(self):
        pass

    @transition(source='*', target=EXPIRED)
    def expire(self):
        pass


def handle_cancellation(sender, *args, **kwargs):
    resource_id = sender.source_id
    try:
        pre_auth = PreAuthorization.objects.get(resource_id=resource_id)
    except PreAuthorization.DoesNotExist, e:
        logger.exception('Received callback for non-existant PreAuthorization object')
    else:
        pre_auth.cancel()

def handle_expiry(sender, *args, **kwargs):
    resource_id = sender.source_id
    try:
        pre_auth = PreAuthorization.objects.get(resource_id=resource_id)
    except PreAuthorization.DoesNotExist, e:
        logger.exception('Received callback for non-existant PreAuthorization object')
    else:
        pre_auth.expire()

signals.pre_authorization_cancelled.connect(handle_cancellation)
signals.pre_authorization_expired.connect(handle_expiry)









