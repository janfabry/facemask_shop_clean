from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from oscar.apps.dashboard.orders import views as oscar_views
from oscar.core.loading import get_model

from facemask_shop.dashboard.orders.forms import FacemaskEditorForm
from facemask_shop.editor.models import Facemask

Order = get_model('order', 'Order')
Line = get_model('order', 'Line')
LineAttribute = get_model('order', 'LineAttribute')


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


class LineEditView(oscar_views.LineDetailView):
    template_name = 'dashboard/orders/line_edit.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['facemask'] = self.get_facemask(kwargs.get('object'))
        context_data['original_facemask'] = self.get_facemask(kwargs.get('object'), 'original-mask-image-id')
        context_data.setdefault('facemask_form', FacemaskEditorForm(initial={'redirect_url': self.request.GET.get('redirect_url')}))
        return context_data

    def get_facemask(self, line: Line, attribute='mask-image-id') -> Facemask:
        try:
            mask_image_id = line.attributes.get(type=attribute).value
        except LineAttribute.DoesNotExist:
            return None
        try:
            facemask = Facemask.objects.get(pk=mask_image_id)
        except Facemask.DoesNotExist:
            return None
        return facemask

    def post(self, request, *args, **kwargs):
        line = self.get_object()
        order = line.order
        form = FacemaskEditorForm(request.POST)
        if form.is_valid():
            facemask_id = form.cleaned_data['facemask_id']
            la = line.attributes.get(type='mask-image-id')
            # Save original mask image ID (if not already saved)
            line.attributes.get_or_create(
                type='original-mask-image-id',
                defaults={
                    'value': la.value
                }
            )
            la.value = facemask_id
            la.save()
            # Invalidate order PDF
            order.print_file = None
            order.save()
            redirect_url = form.cleaned_data.get('redirect_url')
            if not redirect_url:
                redirect_url = reverse('dashboard:order-detail', kwargs={'number': order.number})
            return HttpResponseRedirect(redirect_url)
        else:
            context = self.get_context_data(object=line, facemask_form=form)
            return self.render_to_response(context)
