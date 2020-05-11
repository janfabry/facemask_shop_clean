from django.urls import path

from facemask_shop.editor.views import upload_facemask

app_name = 'editor'
urlpatterns = [
    path('upload/', upload_facemask, name='upload'),
]
