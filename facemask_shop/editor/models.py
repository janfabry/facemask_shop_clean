from django.db import models


class Facemask(models.Model):
    full_image = models.ImageField(upload_to='facemask/full_image/')
    thumbnail = models.ImageField(upload_to='facemask/thumbnail/', blank=True, null=True)
