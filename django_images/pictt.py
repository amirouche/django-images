# -*- coding: utf-8 -*-
from PIL import Image
from cStringIO import StringIO

from django.core.files.storage import default_storage

from resizeimage import resizeimage

from .models import Picture
from .settings import PICTURE_FORMATS


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
    filename = folder + '/' + filename
    default_storage.save(filename, filelike)


def save(input_file, filename, ptype):
    obj = PICTURE_FORMATS[str(ptype)]
    img = Image.open(input_file)
    picture = Picture()
    picture.ptype = ptype
    picture.name = filename
    picture.ext = img.format.lower()
    for key, value in obj['sizes'].items():
        resized_img = resize_img(img, value)
        setattr(picture, key + '_width', resized_img.size[0])
        setattr(picture, key + '_height', resized_img.size[1])
        save_img(resized_img, obj['folder'], filename)
    setattr(picture, 'og_width', img.size[0])
    setattr(picture, 'og_height', img.size[1])
    save_img(img, obj['folder'], filename)
    picture.save()
    return picture
