import json
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import get_model
from django_fsm.db.fields import FSMField, transition
from django_gocardless.client import get_client
from django_gocardless.utils import logger


class ReturnTripManager(models.Manager):
    def from_state(self, state):
        # The state should just hold the ReturnTrip PK
        return self.get(pk=state)

    def create_for_model(self, model_inst, **kwargs):
        return self.create(
            for_model_class="%s.%s" % (model_inst._meta.app_label, model_inst._meta.object_name),
            for_pk=model_inst.pk,
            **kwargs
        )


class ReturnTrip(models.Model):
    """ Stores information relating to a return trip to GoCardless
    """

    DEPARTED = 'departed'
    RETURNED = 'returned'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (DEPARTED, 'Departed'),
        (RETURNED, 'Returned'),
        (CANCELLED, 'Cancelled'),
    )

    created = models.DateTimeField(auto_now=True)
    for_model_class = models.CharField(max_length=100)
    for_pk = models.IntegerField()
    status = FSMField(default='departed')
    extra_state = models.CharField(max_length=255, default='', blank=True)
    success_uri = models.URLField()
    cancel_uri = models.URLField()
    returning_payload_json = models.TextField(default='')
    # Use a TextField as it may be a long URI
    departure_uri = models.TextField(null=True, default=None)
    internal_redirect_uri = models.URLField(null=True, default=None)
    is_signed = models.BooleanField(default=True)

    objects = ReturnTripManager()

    def get_model(self):
        return get_model(*self.for_model_class.split('.')).objects.get(pk=self.for_pk)

    @transition(status, source=DEPARTED, target=RETURNED, save=True)
    def receive(self, request, payload):
        model = self.get_model()
        self.returning_payload_json = json.dumps(payload)

        # Inform the model that the user has returned
        model.user_returns(request, payload, self)
        model.save()

    @transition(status, source=DEPARTED, target=CANCELLED, save=True)
    def cancel(self):
        pass

    @property
    def returning_payload(self):
        return json.loads(self.returning_payload_json)

    def get_departure_uri(self):
        if not self.departure_uri:
            redirect_uri = '%s%s' % (settings.GOCARDLESS_RETURN_ROOT, reverse('gocardless_redirect_return'))
            cancel_uri = '%s?cancel=1&state=%s' % (redirect_uri, self.pk)
            self.departure_uri = self.get_model().make_departure_uri(redirect_uri=redirect_uri, cancel_uri=cancel_uri, state=str(self.pk))
            self.internal_redirect_uri = redirect_uri
            self.save()
        return self.departure_uri
    get_departure_uri.alters_data = True


class ReturnTrippableMixin(object):

    def make_departure_uri(self, redirect_uri, cancel_uri, state):
        raise NotImplementedError()

    def user_returns(self, request, payload, return_trip):
        raise NotImplementedError()