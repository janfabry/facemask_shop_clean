from oscar.apps.shipping.repository import Repository as OscarRepository

from . import methods


class Repository(OscarRepository):
    methods = (methods.Standard(),)
