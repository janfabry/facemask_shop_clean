from django.urls import path

from facemask_shop.editor.views import upload_facemask

urlpatterns = [
    path('upload/', upload_facemask),
]
