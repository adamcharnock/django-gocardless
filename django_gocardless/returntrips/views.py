from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django_gocardless.returntrips.models import ReturnTrip
from django_gocardless.views import GoCardlessView


class ReturnView(GoCardlessView):
    
    def get(self, request, *args, **kwargs):
        # We've come back from GoCardless
        state = request.GET.get('state')
        try:
            # Get the return trip object that tracks what we are doing
            return_trip = ReturnTrip.objects.get(pk=state)
        except ReturnTrip.DoesNotExist:
            # Oops, doesn't exist for some reason
            return HttpResponseBadRequest('Return trip not found. Perhaps state is invalid?')

        #
        return_trip.receive(request, self.get_payload(request))
        success_url = return_trip.success_url
        return HttpResponseRedirect(success_url)

return_view = csrf_exempt(ReturnView.as_view())