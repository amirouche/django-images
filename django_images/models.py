import PIL
import sys
from uuid import uuid4
from json import loads
from json import dumps
try:
    from cStringIO import StringIO
except ImportError:
    # StringIO was replaced by io module in py3
    from io import BytesIO as StringIO

from collections import namedtuple

from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

from resizeimage import resizeimage


if sys.version_info > (3, 0):
    PY3 = True
else:
    PY3 = False


SIZES = ('xs', 'sm', 'md', 'lg', 'og')
Specification = namedtuple('Specification', ('method', 'size'))


class ImageManager(models.Manager):
    """Dynamic manager that filters objects based on the class name

    This is useful to use in combination with proxy models where the name
    of the class is stored as `kind` field, so that only proxy models of the
    given model appear inside of the django admin list"""

    def get_queryset(self):
        kind = self.model.__name__
        return super(ImageManager, self).get_queryset().filter(kind=kind)


class Specification(object):
    """Wraps specification and allow to access resized image atribute

    The name describe the fact that at declaration time it used to specify
    the images resize method and size. At runtime it also manage fetching
    the actual values associated with the specification.
    """

    def __init__(self, method, size):
        self.method = method
        self.size = size
        # set by model construtor
        self.klass = None
        self.name = None

    def __repr__(self):
        """Human readable message to identify the object"""
        return '<Specification class:%s name:%s>' % (self.klass, self.name)

    def __get__(self, model, cls=None):
        """Retrieve the infos dictionary for this image. Since the returned
        value is cached, make sure the model is properly setup before accessing
        `SIZES` attributes."""
        if model is None:
            # `Specification` instance is accessed through a class
            return self
        else:
            try:
                return getattr(model, self.name + '_cache')
            except AttributeError:
                value = loads(getattr(model, 'json_' + self.name))
                value['url'] = settings.MEDIA_URL + value['filepath']
                setattr(model, self.name + '_cache', value)
                return value


def store(pil_image, filepath):
    """Store image on django's `default_storage`"""
    stringio = StringIO()
    pil_image.save(stringio, pil_image.format)
    default_storage.save(filepath, stringio)


class Image(models.Model):
    """Manage all images for the application"""
    kind = models.CharField(max_length=255)
    uid = models.CharField(max_length=255)
    ext = models.CharField(max_length=5)

    json_xs = models.TextField()
    json_sm = models.TextField()
    json_md = models.TextField()
    json_lg = models.TextField()
    json_og = models.TextField()

    # original image field, it's not part of the specification
    # so it won't appear in child proxy models
    og = Specification(method=None, size=None)

    objects = ImageManager()

    def __init__(self, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)

        # finish `Specification` initialization
        for name in SIZES:
            spec = getattr(type(self), name)
            spec.name = name
            spec.klass = type(self).__name__

    def __unicode__(self):
        return str(self.pk)

    @classmethod
    def specs(cls):
        """Retrieve image specifications.

        Those must be declared in child proxy model class"""
        try:
            return cls._specs
        except AttributeError:
            cls._specs = [getattr(cls, x) for x in SIZES]
            return cls._specs

    @classmethod
    def create(cls, image):
        """Save original image `image` and generate resized images.

        Return a `Image` instance for the image"""
        # workaround different byte handling in py3
        if PY3:
            try:
                fd = image.file.file.raw
            except AttributeError:
                # During tests file is backed by a buffer
                fd = image.file.buffer.raw
        else:
            fd = image
        image = PIL.Image.open(fd)
        # prepare django Image model instance
        model = cls()
        model.kind = cls.__name__
        model.ext = image.format.lower()

        # generate unique identifier uid
        while True:
            uid = uuid4().hex
            filepath = "%s.%s" % (uid, image.format.lower())
            # if the original file doesn't exists
            # it means we have a valid uid
            if not default_storage.exists(filepath):
                break
        model.uid = uid

        # cache infos
        infos = dict(
            width=image.size[0],
            heigth=image.size[1],
            filepath=filepath
        )
        model.json_og = dumps(infos)
        # store original image
        store(image, filepath)

        # generate and store other sizes
        for spec in cls.specs():
            # special cased og ie. the original image is already
            # saved above
            if spec.name == 'og':
                continue

            # resize image
            method = 'resize_%s' % spec.method
            method = getattr(resizeimage, method)
            # Don't add `validate=False` if the method doesn't support
            # validation
            # FIXME: should be fixed in python-resize-image
            if hasattr(method, 'validate'):
                resized = method(image, spec.size, validate=False)
            else:
                resized = method(image, spec.size)
            # cache infos
            filepath = "%s_%s.%s" % (
                uid,
                spec.name,
                resized.format.lower()
            )
            infos = dict(
                width=resized.size[0],
                heigth=resized.size[1],
                filepath=filepath
            )
            setattr(model, 'json_' + spec.name, dumps(infos))
            # store
            store(resized, filepath)
        model.save()
        return model

    def delete(self):
        """Delete generated images from the storage backend"""
        super(Image, self).delete()
        for url in [getattr(self, x)['filepath'] for x in SIZES]:
            default_storage.delete(url)

    def all(self):
        """Returns all resized images specification plus the original image as a dict"""
        return {x: getattr(self, x) for x in SIZES}


class CoverImage(Image):

    class Meta:
        proxy = True

    xs = Specification(method='cover', size=(105, 60))
    sm = Specification(method='cover', size=(350, 230))
    md = Specification(method='cover', size=(525, 345))
    lg = Specification(method='cover', size=(1050, 690))


class ContentImage(Image):

    class Meta:
        proxy = True

    xs = Specification(method='width', size=50)
    sm = Specification(method='width', size=120)
    md = Specification(method='width', size=200)
    lg = Specification(method='width', size=400)


class PictoImage(Image):

    class Meta:
        proxy = True

    xs = Specification(method='cover', size=(10, 10))
    sm = Specification(method='cover', size=(20, 20))
    md = Specification(method='cover', size=(30, 30))
    lg = Specification(method='cover', size=(35, 35))


class LogoImage(Image):

    class Meta:
        proxy = True

    xs = Specification(method='contain', size=(50, 21))
    sm = Specification(method='contain', size=(100, 50))
    md = Specification(method='contain', size=(150, 62))
    lg = Specification(method='contain', size=(200, 83))
