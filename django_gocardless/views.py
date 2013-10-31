import json
import logging
from django.conf import settings
from django.http.response import HttpResponseBadRequest
from django.views.generic.base import View, logger
from gocardless.utils import generate_signature

class GoCardlessPayloadMixin(object):

    def get_payload(self, request):
        if not hasattr(self, '_payload'):
            if request.method.lower() == 'get':
                self._payload = request.GET.dict()
            else:
                self._payload = json.loads(request.body)['payload']
        return self._payload

class GoCardlessSignatureMixin(GoCardlessPayloadMixin):
    """ Will verify a GoCardless signature """
    manual_signature_check = False

    def verify_signature(self, request):
        data = self.get_payload(request)
        if not data:
            logger.warning('No payload or request data found')
            return False

        pms = data.copy()
        pms.pop('signature')
        signature = generate_signature(pms, settings.GOCARDLESS_APP_SECRET)

        if signature == data['signature']:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.manual_signature_check and not self.verify_signature(request):
            return self.handle_invalid_signature(request, *args, **kwargs)

        return super(GoCardlessSignatureMixin, self).dispatch(request, *args, **kwargs)

    def handle_invalid_signature(self, request, *args, **kwargs):
        return HttpResponseBadRequest('Signature did not validate')


class GoCardlessView(GoCardlessSignatureMixin, View):
    pass