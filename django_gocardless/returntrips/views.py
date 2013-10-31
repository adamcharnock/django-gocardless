from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import RedirectView

from django_gocardless.returntrips.models import ReturnTrip
from django_gocardless.views import GoCardlessView


class ReturnView(GoCardlessView):
    manual_signature_check = True

    def get(self, request, *args, **kwargs):
        # We've come back from GoCardless
        state = request.GET.get('state')
        try:
            state = int(state)
        except (ValueError, TypeError):
            return HttpResponseBadRequest('Invalid state')

        try:
            # Get the return trip object that tracks what we are doing
            return_trip = ReturnTrip.objects.get(pk=state)
        except ReturnTrip.DoesNotExist:
            # Oops, doesn't exist for some reason
            return HttpResponseBadRequest('Return trip not found. Perhaps state is invalid?')

        # Manually check the signature if this return trip expects one
        if return_trip.is_signed and not self.verify_signature(request):
            return self.handle_invalid_signature(request, *args, **kwargs)

        return_trip.receive(request, self.get_payload(request))
        success_url = return_trip.success_uri
        if return_trip.extra_state:
            success_url += '?state=%s' % return_trip.extra_state
        return HttpResponseRedirect(success_url)

return_view = csrf_exempt(ReturnView.as_view())


class GoCardlessDepartureView(RedirectView):
    permanent = False
    # Specify in child class
    form = None

    def get(self, request, *args, **kwargs):
        form = self.form(self.request.GET)
        if not form.is_valid():
            context = RequestContext(self.request, dict(form=form))
            return render_to_response('gocardless/preauthorizations/depart_error.html', context_instance=context)
        else:
            kwargs['form'] = form
            return super(GoCardlessDepartureView, self).get(request, *args, **kwargs)