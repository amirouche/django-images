# -*- coding: utf-8 -*-
import PIL
from uuid import uuid4
from cStringIO import StringIO

from django.core.files.storage import default_storage

from resizeimage import resizeimage

from .models import Image
from .settings import IMAGE_FORMATS


def unique_filepath(folder, filename):
    filepath = folder + '/' + filename
    if not default_storage.exists(filepath):
        return filepath
    else:
        while True:
            filepath = folder + '/' + uuid4().hex
            filepath += '-' + filename
            if not default_storage.exists(filepath):
                return filepath


def resize_img(image_file, params):
    return getattr(
        resizeimage,
        'resize_%s' % params['method']
    )(image_file, params['size'])


def save_img(image_file, folder, filename):
    size = image_file.size
    filelike = StringIO()
    image_file.save(filelike, image_file.format)
    filename = "%s_%sx%s.%s" % (
        filename,
        size[0],
        size[1],
        image_file.format.lower()
    )
    filepath = unique_filepath(folder, filename)
    default_storage.save(filepath, filelike)


def save(input_file, filename, ptype):
    obj = IMAGE_FORMATS[str(ptype)]
    img = PIL.Image.open(input_file)
    image = Image()
    image.ptype = ptype
    image.name = filename
    image.ext = img.format.lower()
    for key, value in obj['sizes'].items():
        resized_img = resize_img(img, value)
        setattr(image, key + '_width', resized_img.size[0])
        setattr(image, key + '_height', resized_img.size[1])
        save_img(resized_img, obj['folder'], filename)
    setattr(image, 'og_width', img.size[0])
    setattr(image, 'og_height', img.size[1])
    save_img(img, obj['folder'], filename)
    image.save()
    return image
