from django.http import Http404, HttpResponseRedirect
from django.views.generic import DetailView
from oscar.core.loading import get_model

from facemask_shop.editor.models import Facemask

Line = get_model('order', 'Line')
LineAttribute = get_model('order', 'LineAttribute')


class LineImageView(DetailView):
    model = Line

    def get_queryset(self):
        if self.request.user.is_staff:
            return Line._default_manager.all()
        if self.request.user.is_anonymous:
            return Line._default_manager.none()
        return Line._default_manager.filter(order__user=self.request.user)

    def get(self, request, *args, **kwargs):
        line = self.get_object()
        try:
            mask_image_id = line.attributes.get(type='mask-image-id').value
        except LineAttribute.DoesNotExist:
            raise Http404('No mask-image-id line attribute')
        try:
            facemask = Facemask.objects.get(pk=mask_image_id)
        except Facemask.DoesNotExist:
            raise Http404('No facemask')
        return HttpResponseRedirect(self.get_image(facemask))


class LineThumbnailView(LineImageView):
    def get_image(self, facemask):
        facemask.create_thumbnail()
        return facemask.thumbnail.url


class LineFullView(LineImageView):
    def get_image(self, facemask):
        facemask.create_mask_image()
        return facemask.mask_image.url
