from django import forms

from facemask_shop.editor.models import Facemask


class FacemaskForm(forms.ModelForm):
    class Meta:
        model = Facemask
        fields = forms.ALL_FIELDS
