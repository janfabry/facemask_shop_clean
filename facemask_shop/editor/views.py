from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from facemask_shop.editor.forms import FacemaskForm


@csrf_exempt
def upload_facemask(request):
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = ', '.join((
            "accept",
            "accept-encoding",
            "authorization",
            "content-type",
            "dnt",
            "origin",
            "user-agent",
            "x-csrftoken",
            "x-requested-with",
        ))
        response['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
        return response
    if request.method == 'POST':
        form = FacemaskForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            facemask = form.save()
            response = JsonResponse({'success': True, 'mask_id': facemask.id})
        else:
            response = JsonResponse({'success': False, 'errors': form.errors}, status=400)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    return HttpResponseNotAllowed(permitted_methods=('POST',))
