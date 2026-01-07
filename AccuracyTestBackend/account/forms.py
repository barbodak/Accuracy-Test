from django import forms
from .models import Organization


class BulkCreateForm(forms.Form):
    number_of_accounts = forms.IntegerField(
        label="Number of accounts", min_value=1, initial=10
    )
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(), required=True
    )
    acuTest_permission = forms.BooleanField(required=False, label="AcuTest Permission")
    valuTest_permission = forms.BooleanField(
        required=False, label="ValuTest Permission"
    )
