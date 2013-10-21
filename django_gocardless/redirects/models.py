from django.db import models
from django.db.models import get_model
from django_fsm.db.fields import FSMField, transition


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

    objects = ReturnTripManager()

    def get_model(self):
        return get_model(*self.for_model_class.split('.')).objects.get(pk=self.for_pk)

    @transition(source='departed', target='returned', save=True)
    def receive(self):
        model = self.get_model()
        model.user_returns(self)
        model.save()



