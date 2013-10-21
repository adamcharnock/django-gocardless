from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django_gocardless.views import GoCardlessView

from .models import Payload


class WebhookView(GoCardlessView):

    def post(self, request, *args, **kwargs):
        Payload.objects.create_for_payload(self.get_payload(request))
        return HttpResponse('OK')

    def handle_invalid_signature(self, request, *args, **kwargs):
        Payload.objects.create_for_payload(self.get_payload(request), flag='Signature did not validate')
        return super(WebhookView, self).handle_invalid_signature(request, *args, **kwargs)


webhook_view = csrf_exempt(WebhookView.as_view())
