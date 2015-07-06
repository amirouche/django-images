from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

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

    def delete(self):
        """Delete generated images from the storage backend"""
        super(Image, self).delete()
        for url in map(self.relativeurl, ('xs', 'sm', 'md', 'lg', 'og')):
            default_storage.delete(url)

    def __unicode__(self):
        """Human readable message to identify the object"""
        return self.name

    def relativeurl(self, size):
        """path relative to the root directory where images are served

        This is by default MEDIA_URL"""
        folder = IMAGE_FORMATS[str(self.ptype)]['folder']
        url = '%s/%s' % (folder, self.filename(size))
        return url

    def url(self, size):
        """Return the full url for a given size"""
        url = settings.MEDIA_URL
        url += self.relativeurl(size)
        return url

    def filename(self, size):
        """Return the filename of an image for a given size"""
        filepath = "%s_%sx%s.%s" % (
            self.uid,
            getattr(self, size + '_width'),
            getattr(self, size + '_height'),
            self.ext,
        )
        return filepath

    @property
    def allrelativeurl(self):
        """Return all relative urls"""
        arr = []
        arr.append(self.relativeurl('xs'))
        arr.append(self.relativeurl('sm'))
        arr.append(self.relativeurl('md'))
        arr.append(self.relativeurl('lg'))
        arr.append(self.relativeurl('og'))
        return arr

    def image_dict(self, size):
        """Return dictionary with url, width, height for a given size"""
        return {
            "url": self.url(size),
            "width": getattr(self, size + '_width'),
            "height": getattr(self, size + '_height')
        }

    @property
    def xs(self):
        """Dict for `xs` size."""
        return self.image_dict('xs')

    @property
    def sm(self):
        """Dict for `sm` size."""
        return self.image_dict('sm')

    @property
    def md(self):
        """Dict for `md` size."""
        return self.image_dict('md')

    @property
    def lg(self):
        """Dict for `lg` size."""
        return self.image_dict('lg')

    @property
    def og(self):
        """Dict for `og` size."""
        return self.image_dict('og')

    def todict(self):
        """Serialize the object to a dict."""
        res = {}
        res['xs'] = self.xs
        res['sm'] = self.sm
        res['md'] = self.md
        res['lg'] = self.lg
        res['og'] = self.og
        return res
