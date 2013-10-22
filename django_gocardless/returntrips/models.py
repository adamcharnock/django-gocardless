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

    created = models.DateTimeField(auto_now=True)
    for_model_class = models.CharField(max_length=100)
    for_pk = models.IntegerField()
    status = FSMField(default='departed')
    extra_state = models.CharField(max_length=255, default='', blank=True)
    depart_url = models.CharField(max_length=255)
    success_url = models.URLField()
    cancel_url = models.URLField()
    returning_payload_json = models.TextField(default='')

    objects = ReturnTripManager()

    def get_model(self):
        return get_model(*self.for_model_class.split('.')).objects.get(pk=self.for_pk)

    @transition(source='departed', target='returned', save=True)
    def receive(self, request, payload):
        model = self.get_model()
        self.returning_payload_json = json.dumps(payload)

        # Log that we have returned
        model.user_returns(self)
        model.save()

        # Now confirm
        try:
            get_client().confirm_resource(payload)
        except:
            logger.exception('Failed to confirm resource on return trip')
        else:
            model.activate()
            model.save()

    @property
    def returning_payload(self):
        return json.loads(self.returning_payload_json)

    def get_departure_url(self):
        redirect_uri = '%s%s' % (settings.GOCARDLESS_RETURN_ROOT, reverse('gocardless_redirect_return'))
        return self.get_model().make_authorize_url(redirect_uri=redirect_uri, state=str(self.pk))


class ReturnTrippableMixin(object):

    def make_authorize_url(self, redirect_uri, state):
        raise NotImplementedError()

    def user_returns(self, return_trip):
        raise NotImplementedError()

    def activate(self):
        raise NotImplementedError()
