from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from oscar.core.loading import get_model

Product = get_model('catalogue', 'product')


class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = {
            label: Product.objects.get(pk=int(pk))
            for label, pk in
            settings.FACEMASKME_PRODUCT_IDS.items()
        }
        return context
