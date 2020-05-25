import oscar.apps.catalogue.apps as apps
from django.conf.urls import url
from django.urls import include


class CatalogueConfig(apps.CatalogueConfig):
    name = 'facemask_shop.catalogue'
