import oscar.apps.dashboard.orders.apps as apps
from django.conf.urls import url
from oscar.core.loading import get_class


class OrdersDashboardConfig(apps.OrdersDashboardConfig):
    name = 'facemask_shop.dashboard.orders'

    def ready(self):
        super().ready()
        self.permissions_map['order-pdf'] = (['is_staff'], ['partner.dashboard_access'])
        self.pdf_view = get_class('dashboard.orders.views', 'PdfView')
        self.line_edit_view = get_class('dashboard.orders.views', 'LineEditView')

    def get_urls(self):
        urls = [
            url(r'^$', self.order_list_view.as_view(), name='order-list'),
            url(r'^statistics/$', self.order_stats_view.as_view(),
                name='order-stats'),
            url(r'^(?P<number>[-\w]+)/$',
                self.order_detail_view.as_view(), name='order-detail'),
            url(r'^(?P<number>[-\w]+)/notes/(?P<note_id>\d+)/$',
                self.order_detail_view.as_view(), name='order-detail-note'),
            url(r'^(?P<number>[-\w]+)/lines/(?P<line_id>\d+)/$',
                self.line_detail_view.as_view(), name='order-line-detail'),
            url(r'^(?P<number>[-\w]+)/shipping-address/$',
                self.shipping_address_view.as_view(),
                name='order-shipping-address'),
            url(r'^(?P<number>[-\w]+)/pdf/$',
                self.pdf_view.as_view(),
                name='order-pdf'),
            url(r'^(?P<number>[-\w]+)/lines/(?P<line_id>\d+)/edit/$',
                self.line_edit_view.as_view(),
                name='order-line-edit'),
        ]
        return self.post_process_urls(urls)
