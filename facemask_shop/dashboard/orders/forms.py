from django import forms


class FacemaskEditorForm(forms.Form):
    facemask_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    redirect_url = forms.URLField(required=False, widget=forms.HiddenInput())
