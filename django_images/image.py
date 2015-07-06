# -*- coding: utf-8 -*-
import PIL
from uuid import uuid4
from cStringIO import StringIO

from django.core.files.storage import default_storage

from resizeimage import resizeimage

from .models import Image
from .settings import IMAGE_FORMATS


def store(pil_image, filepath):
    stringio = StringIO()
    pil_image.save(stringio, pil_image.format)
    default_storage.save(filepath, stringio)


def save(input_file, filename, ptype):
    obj = IMAGE_FORMATS[str(ptype)]
    img = PIL.Image.open(input_file)
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
