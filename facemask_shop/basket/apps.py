import oscar.apps.basket.apps as apps
from django.conf.urls import url
from oscar.core.loading import get_class


class BasketConfig(apps.BasketConfig):
    name = 'facemask_shop.basket'

    def ready(self):
        super().ready()
        self.line_thumbnail_view = get_class('basket.views', 'LineThumbnailView')
        self.line_full_view = get_class('basket.views', 'LineFullView')

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            url(r'^line/(?P<pk>\d+)/thumbnail/$', self.line_thumbnail_view.as_view(), name='line-thumbnail'),
            url(r'^line/(?P<pk>\d+)/full/$', self.line_full_view.as_view(), name='line-full'),
        ]
        return self.post_process_urls(urls)
