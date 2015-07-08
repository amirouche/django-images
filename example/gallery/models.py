from django.db import models

from django_images.models import Image
from django_images.models import Specification


class BackgroundImage(Image):

    class Meta:
        proxy = True

    xs = Specification(method='width', size=100)
    sm = Specification(method='width', size=300)
    md = Specification(method='width', size=600)
    lg = Specification(method='width', size=1000)


class Logo(Image):

    class Meta:
        proxy = True

    xs = Specification(method='contain', size=(24, 24))
    sm = Specification(method='contain', size=(50, 50))
    md = Specification(method='contain', size=(100, 100))
    lg = Specification(method='contain', size=(400, 400))


# Example of foreign key use


class Vitrine(models.Model):

    title = models.CharField(max_length=255)
    logo = models.ForeignKey(Logo)
    background = models.ForeignKey(BackgroundImage)
