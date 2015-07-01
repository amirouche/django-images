from django.db import models
from django.conf import settings as SETTINGS
import os


PICTURE_CHOICES = [[int(key), value['display']] for key, value in SETTINGS.PICTURES.items()]

class Picture(models.Model):
    """
    manage all images for the application
    """
    ptype = models.SmallIntegerField(choices=PICTURE_CHOICES)
    name = models.CharField(max_length=255)
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

    def relativeurl(self, sz):
        return os.path.join(SETTINGS.PICTURES[str(self.ptype)]['folder'], self.filename(sz))

    def url(self, size):
        return os.path.join(SETTINGS.S3_ENDPOINT, self.relativeurl(size))

    def filename(self, sz):
    	return '%s_%sx%s.%s' % (self.name, getattr(self, sz + '_width'), getattr(self, sz + '_height'), self.ext)

    @property
    def allrelativeurl(self):
        arr = []
        arr.append(self.relativeurl('xs'))
        arr.append(self.relativeurl('sm'))
        arr.append(self.relativeurl('md'))
        arr.append(self.relativeurl('lg'))
        arr.append(self.relativeurl('og'))
        return arr

    def picture_dict(self, sz):
    	return {
                "url": self.url(sz),
                "width": getattr(self, sz + '_width'),
                "height": getattr(self, sz + '_height')
            }

    @property
    def xs(self):
        return self.picture_dict('xs')

    @property
    def sm(self):
        return self.picture_dict('sm')

    @property
    def md(self):
        return self.picture_dict('md')

    @property
    def lg(self):
        return self.picture_dict('lg')

    @property
    def og(self):
        return self.picture_dict('og')

    def todict(self):
        res = {}
        res['xs'] = self.xs
        res['sm'] = self.sm
        res['md'] = self.md
        res['lg'] = self.lg
        res['og'] = self.og
        return res