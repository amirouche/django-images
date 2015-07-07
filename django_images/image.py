# -*- coding: utf-8 -*-
import sys
import PIL
from uuid import uuid4
try:
    from cStringIO import StringIO
except ImportError:
    # StringIO was replaced by io module
    from io import BytesIO as StringIO

from django.core.files.storage import default_storage

from resizeimage import resizeimage

from .models import Image
from .settings import IMAGE_FORMATS


if sys.version_info > (3, 0):
    PY3 = True
else:
    PY3 = False


def store(pil_image, filepath):
    """Store image on django's `default_storage`"""
    stringio = StringIO()
    pil_image.save(stringio, pil_image.format)
    default_storage.save(filepath, stringio)


def save(input_file, filename, ptype):
    """Save original image `input_file` and generate resized images.

    Return a `Image` instance for the image"""
    # workaround difference in byte handling in py3
    if PY3:
        try:
            fd = input_file.file.file.raw
        except AttributeError:
            # During tests file is backed by a buffer
            fd = input_file.file.buffer.raw
    else:
        fd = input_file
    obj = IMAGE_FORMATS[str(ptype)]
    img = PIL.Image.open(fd)
    # prepare django Image instance
    image = Image()
    image.ptype = ptype
    image.name = filename
    image.ext = img.format.lower()

    folder = obj['folder']
    # store original image and retrieve uid
    while True:
        uid = uuid4().hex
        filepath = "%s/%s_%sx%s.%s" % (
            folder,
            uid,
            img.size[0],
            img.size[1],
            img.format.lower()
        )
        # if the original file doesn't exists
        # it means we have a valid uid
        if not default_storage.exists(filepath):
            break
    image.uid = uid
    store(img, filepath)
    setattr(image, 'og_width', img.size[0])
    setattr(image, 'og_height', img.size[1])

    # generate and store other sizes
    for key, value in obj['sizes'].items():
        # resize image
        method = 'resize_%s' % value['method']
        method = getattr(resizeimage, method)
        resized = method(img, value['size'], validate=False)
        # cache width/height
        setattr(image, key + '_width', resized.size[0])
        setattr(image, key + '_height', resized.size[1])
        # store
        filepath = "%s/%s_%sx%s.%s" % (
            folder,
            uid,
            resized.size[0],
            resized.size[1],
            resized.format.lower()
        )
        store(resized, filepath)
    image.save()
    return image
