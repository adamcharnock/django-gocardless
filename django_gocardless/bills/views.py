from django.contrib.auth.decorators import login_required
from django_gocardless.bills.forms import BillDepartForm
from django_gocardless.bills.models import Bill
from django_gocardless.returntrips.models import ReturnTrip
from django_gocardless.returntrips.views import GoCardlessDepartureView


class BillDepartView(GoCardlessDepartureView):
    form = BillDepartForm

    def get_redirect_url(self, form, **kwargs):
        data = form.cleaned_data

        to_user = data['to_user']
        bill = Bill.objects.create(
            user=self.request.user,
            to_user=to_user,
            amount=data['amount'],
            name=data['name'],
            description=data['description'],
            user_company_name=data['user_company_name'],
            user_postal_code=data['user_postal_code'],
        )
        return_trip = ReturnTrip.objects.create_for_model(
            bill,
            extra_state=data['state'],
            success_uri=data['redirect_uri'],
            cancel_uri=data['cancel_uri'] or data['redirect_uri'],
            is_signed=False,
        )
        bill.return_trip = return_trip
        bill.save()

        return return_trip.get_departure_uri()

bill_depart_view = login_required(BillDepartView.as_view())