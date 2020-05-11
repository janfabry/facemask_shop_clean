from django import forms

from oscar.apps.basket.forms import AddToBasketForm as OscarAddToBasketForm


class AddToBasketForm(OscarAddToBasketForm):
    def _add_option_field(self, product, option):
        super()._add_option_field(product, option)
        if product.product_class.name == 'Facemask':
            if option.code == 'mask-image-id':
                self.fields[option.code].widget = forms.HiddenInput()


class SimpleAddToBasketForm(AddToBasketForm):
    """
    Overridden again, because the original one extends the Oscar AddToBasketForm,
    not our forked one.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'quantity' in self.fields:
            self.fields['quantity'].initial = 1
            self.fields['quantity'].widget = forms.HiddenInput()
