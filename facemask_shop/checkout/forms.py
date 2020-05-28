from django import forms


class TermsAndConditionsForm(forms.Form):
    agree_to_terms = forms.BooleanField(required=True, label='I agree to the terms and conditions')
