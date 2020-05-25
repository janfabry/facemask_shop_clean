from django.conf import settings

from oscar.core.loading import get_model
from oscar.apps.catalogue.views import ProductDetailView as OscarProductDetailView


Product = get_model('catalogue', 'product')


class ProductDetailView(OscarProductDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = {
            label: Product.objects.get(pk=int(pk))
            for label, pk in
            settings.FACEMASKME_PRODUCT_IDS.items()
        }
        return context
