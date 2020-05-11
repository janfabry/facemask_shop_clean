from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from facemask_shop.editor.forms import FacemaskForm


@csrf_exempt
def upload_facemask(request):
    if request.method == 'POST':
        form = FacemaskForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            facemask = form.save()
            return JsonResponse({'success': True, 'mask_id': facemask.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(permitted_methods=('POST',))
