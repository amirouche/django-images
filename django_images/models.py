from django.db import models
from django.conf import settings

from .settings import IMAGE_FORMATS


IMAGE_CHOICES = [
    [int(key), value['display']] for key, value in IMAGE_FORMATS.items()
]


class Image(models.Model):
    """
    manage all images for the application
    """
    name = models.CharField(max_length=255)
    ptype = models.SmallIntegerField(choices=IMAGE_CHOICES)
    uid = models.CharField(max_length=255)
    ext = models.CharField(max_length=5)
    xs_width = models.SmallIntegerField()
    xs_height = models.SmallIntegerField()
    sm_width = models.SmallIntegerField()
    sm_height = models.SmallIntegerField()
    md_width = models.SmallIntegerField()
    md_height = models.SmallIntegerField()
    lg_width = models.SmallIntegerField()
    lg_height = models.SmallIntegerField()
    og_width = models.SmallIntegerField()
    og_height = models.SmallIntegerField()

    def __unicode__(self):
        return self.name

    def relativeurl(self, size):
        folder = IMAGE_FORMATS[str(self.ptype)]['folder']
        url = '%s/%s' % (folder, self.filename(size))
        return url

    def url(self, size):
        url = settings.MEDIA_URL
        url += self.relativeurl(size)
        return url

    def filename(self, size):
        filepath = "%s_%sx%s.%s" % (
            self.uid,
            getattr(self, size + '_width'),
            getattr(self, size + '_height'),
            self.ext,
        )
        return filepath

    @property
    def allrelativeurl(self):
        arr = []
        arr.append(self.relativeurl('xs'))
        arr.append(self.relativeurl('sm'))
        arr.append(self.relativeurl('md'))
        arr.append(self.relativeurl('lg'))
        arr.append(self.relativeurl('og'))
        return arr

    def image_dict(self, size):
        return {
            "url": self.url(size),
            "width": getattr(self, size + '_width'),
            "height": getattr(self, size + '_height')
        }

    @property
    def xs(self):
        return self.image_dict('xs')

    @property
    def sm(self):
        return self.image_dict('sm')

    @property
    def md(self):
        return self.image_dict('md')

    @property
    def lg(self):
        return self.image_dict('lg')

    @property
    def og(self):
        return self.image_dict('og')

    def todict(self):
        res = {}
        res['xs'] = self.xs
        res['sm'] = self.sm
        res['md'] = self.md
        res['lg'] = self.lg
        res['og'] = self.og
        return res
