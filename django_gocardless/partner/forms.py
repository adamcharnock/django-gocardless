from django import forms


class PartnerDepartForm(forms.Form):
    redirect_uri = forms.URLField()
    state = forms.CharField(max_length=200, required=False)