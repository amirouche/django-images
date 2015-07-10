from django_images.models import Image
from django_images.models import Specification


class TestImage(Image):

    class Meta:
        proxy = True

    xs = Specification(method='height', size=600)
    sm = Specification(method='width', size=600)
    md = Specification(method='cover', size=(500, 500))
    lg = Specification(method='contain', size=(700, 700))
