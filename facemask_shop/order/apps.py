import oscar.apps.order.apps as apps
from django.conf.urls import url
from oscar.core.loading import get_class


class OrderConfig(apps.OrderConfig):
    name = 'facemask_shop.order'

    def ready(self):
        super().ready()
        self.line_thumbnail_view = get_class('order.views', 'LineThumbnailView')
        self.line_full_view = get_class('order.views', 'LineFullView')

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            url(r'^line/(?P<pk>\d+)/thumbnail/$', self.line_thumbnail_view.as_view(), name='line-thumbnail'),
            url(r'^line/(?P<pk>\d+)/full/$', self.line_full_view.as_view(), name='line-full'),
        ]
        return self.post_process_urls(urls)
