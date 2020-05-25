from django.utils.encoding import smart_text
from oscar.apps.basket.abstract_models import AbstractLine


class Line(AbstractLine):
    @property
    def description(self):
        d = smart_text(self.product)
        # Don't show mask image ID (could show other options later)
        return d


from oscar.apps.basket.models import *  # noqa isort:skip
