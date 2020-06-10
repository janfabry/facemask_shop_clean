from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from oscar.apps.dashboard.orders import views as oscar_views

from facemask_shop.order.models import Order


class OrderListView(oscar_views.OrderListView):
    template_name = 'dashboard/orders/order_list.html'


class OrderDetailView(oscar_views.OrderDetailView):
    template_name = 'dashboard/orders/order_detail.html'


class PdfView(DetailView):
    model = Order
    context_object_name = 'order'

    def get_object(self, queryset=None):
        from oscar.apps.dashboard.orders.views import get_order_for_user_or_404
        return get_order_for_user_or_404(
            self.request.user, self.kwargs['number'])

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        order.create_print_file()
        return HttpResponseRedirect(order.print_file.url)
