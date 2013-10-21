from django.db import models
from django_fsm.db.fields import FSMField, transition
from django_gocardless.client import get_client
from django_gocardless.redirects.models import ReturnTrip


class PreAuthorization(models.Model):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'

    INTERVAL_UNIT_CHOICES = (
        (DAY, 'Day'),
        (WEEK, 'Week'),
        (MONTH, 'Month'),
    )

    NOTSENT = 'notsent'
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'

    created = models.DateTimeField(auto_now=True)
    status = FSMField(default='notsent')
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interval_length = models.SmallIntegerField(default=1)
    interval_unit = models.CharField(max_length=10, default=MONTH, choices=INTERVAL_UNIT_CHOICES)
    expires_at = models.DateField(default=None, null=True, blank=True)
    interval_count = models.SmallIntegerField(default=None, blank=True, null=True, help_text='After how many intervals does this pre-auth expire')
    name = models.CharField(max_length=255, blank=True, default='', help_text='Brief description used to identify the pre-authorization, displayed to the user alongside the amount. Often useful for an "invoice reference"')
    description = models.TextField(default='', blank=True, help_text='More verbose description, which will be displayed to the user')
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    calendar_intervals = models.BooleanField(default=False)

    def get_return_trip(self):
        return ReturnTrip.objects.create_for_model(self, depart_url=self.authorize_url)

    @property
    def authorize_url(self):
        client = get_client()
        return client.new_pre_authorization_url(
            self.max_amount,
            self.interval_length,
            self.interval_unit,
            self.expires_at,
            self.name or None,
            self.description or None,
            self.interval_count,
            self.calendar_intervals,
            self.redirect_url,
        )

    @transition(source='notsent', target='inactive')
    def user_returns(self, return_trip):
        pass

    @property
    def success_url(self):
        # Where to go after a successful auth
        # TODO: Implement properly
        return '/pre-auth/done/'



