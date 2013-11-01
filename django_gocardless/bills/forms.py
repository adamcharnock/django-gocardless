from decimal import Decimal
from django import forms
from django.contrib.auth import get_user_model


class BillDepartForm(forms.Form):
    redirect_uri = forms.URLField()
    cancel_uri = forms.URLField(required=False)
    state = forms.CharField(max_length=200, required=False)
    to_user = forms.CharField(max_length=200, required=False)
    amount = forms.DecimalField(max_digits=8, decimal_places=2, min_value=Decimal('0.01'))
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=1000, required=False)
    user_company_name = forms.CharField(max_length=100, required=False)
    user_postal_code = forms.CharField(max_length=100, required=False)

    def clean_to_user(self):
        to_user = self.cleaned_data['to_user']
        if not to_user:
            return None

        try:
            to_user = get_user_model().objects.get(pk=to_user)
        except get_user_model().DoesNotExist:
            raise forms.ValidationError('User specified by "to_user" could not be found')

        return to_user