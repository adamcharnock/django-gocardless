from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django_gocardless.redirects.models import ReturnTrip
from django_gocardless.views import GoCardlessView


class ReturnView(GoCardlessView):
    
    def get(self, request, *args, **kwargs):
        try:
            return_trip = ReturnTrip.objects.get(pk=request.GET.get('state'))
        except ReturnTrip.DoesNotExist:
            return HttpResponseBadRequest('Return trip not found')
        return_trip.receive()
        success_url = return_trip.get_model().success_url
        return HttpResponseRedirect(success_url)

return_view = csrf_exempt(ReturnView.as_view())