import json
from django.conf import settings
from django.http.response import HttpResponseBadRequest
from django.views.generic.base import View
from gocardless.utils import generate_signature

class GoCardlessPayloadMixin(object):

    def get_payload(self, request):
        if not getattr(self, '_payload', None):
            self._payload = json.loads(request.body)['payload']
        return self._payload

class GoCardlessSignatureMixin(GoCardlessPayloadMixin):
    """ Will verify a GoCardless signature """

    def verify_signature(self, request):
        payload = self.get_payload(request)
        pms = payload.copy()
        pms.pop('signature')
        signature = generate_signature(pms, settings.GOCARDLESS_APP_SECRET)

        if signature == payload['signature']:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() not in ('GET', 'HEAD'):
            if not self.verify_signature(request):
                return self.handle_invalid_signature(request, *args, **kwargs)

        return super(GoCardlessSignatureMixin, self).dispatch(request, *args, **kwargs)

    def handle_invalid_signature(self, request, *args, **kwargs):
        return HttpResponseBadRequest('Signature did not validate')


class GoCardlessView(GoCardlessSignatureMixin, View):
    pass