from django.contrib.auth.decorators import login_required
from django_gocardless.partners.forms import PartnerDepartForm
from django_gocardless.partners.models import PartnerMerchant
from django_gocardless.returntrips.models import ReturnTrip
from django_gocardless.returntrips.views import GoCardlessDepartureView


class PartnerDepartView(GoCardlessDepartureView):
    form = PartnerDepartForm

    def get_redirect_url(self, form, **kwargs):
        data = form.cleaned_data
        partner_merchant = PartnerMerchant.objects.create(
            user=self.request.user,
        )
        return_trip = ReturnTrip.objects.create_for_model(
            partner_merchant,
            extra_state=data['state'],
            success_uri=data['redirect_uri'],
            cancel_uri=data['redirect_uri'],
            is_signed=False,
        )
        partner_merchant.return_trip = return_trip
        partner_merchant.save()

        return return_trip.get_departure_uri()

partner_depart_view = login_required(PartnerDepartView.as_view())