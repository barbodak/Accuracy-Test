from django import forms
from .models import Organization


class BulkCreateForm(forms.Form):
    number_of_accounts = forms.IntegerField(
        label="Number of accounts", min_value=1, initial=10
    )
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(), required=True
    )
    acuTest_permition = forms.BooleanField(required=False, label="AcuTest Permission")
    valTest_permition = forms.BooleanField(required=False, label="ValTest Permission")
