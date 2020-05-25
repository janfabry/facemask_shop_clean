import oscar.apps.catalogue.apps as apps
from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView


class CatalogueConfig(apps.CatalogueConfig):
    name = 'facemask_shop.catalogue'

    def get_urls(self):
        urls = [
            url(r'^$', RedirectView.as_view(url=reverse_lazy('home')), name='index'),
            url(r'^(?P<product_slug>[\w-]*)_(?P<pk>\d+)/$',
                self.detail_view.as_view(), name='detail'),
            url(r'^category/(?P<category_slug>[\w-]+(/[\w-]+)*)_(?P<pk>\d+)/$',
                RedirectView.as_view(url=reverse_lazy('home')), name='category'),
            url(r'^ranges/(?P<slug>[\w-]+)/$',
                RedirectView.as_view(url=reverse_lazy('home')), name='range'),
        ]
        return self.post_process_urls(urls)
