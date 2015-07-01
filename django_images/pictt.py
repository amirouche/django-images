# -*- coding: utf-8 -*-
from django.conf import settings as SETTINGS
from PIL import Image
from pictures.models import Picture
from cStringIO import StringIO
import requests
from imageresize import imageresize, imageexceptions
from components import s3 as S3
from pictures import picttexceptions


def imgfromurl(url):
    try:
        r = requests.get(url)
    except requests.ConnectionError as e:
        raise picttexceptions.URLError(e)
    except requests.HTTPError as e:
        raise picttexceptions.URLError(e)
    else:
        img = StringIO(r.content)
    return img


def resize_img(image_file, params):
    return getattr(
        imageresize,
        'resize_%s' % params['method']
    )(image_file, params['size'])


def save_img(image_file, folder, filename):
    size = image_file.size
    filename = "%s_%sx%s.%s" % (
        filename, size[0], size[1], image_file.format.lower())
    filelike = StringIO()
    image_file.save(filelike, image_file.format)
    S3.save(filelike, folder, filename)


def save(input_file, filename, ptype):
    obj = SETTINGS.PICTURES[str(ptype)]
    img = Image.open(input_file)
    picture = Picture()
    picture.ptype = ptype
    picture.name = filename
    picture.ext = img.format.lower()
    for key, value in obj['sizes'].items():
        try:
            resized_img = resize_img(img, value)
        except imageexceptions.ImageSizeError as e:
            S3.delete_all(picture.allrelativeurl)
            raise picttexceptions.ImageSizeError(
                e.actual_size, e.required_size)
        else:
            setattr(picture, key + '_width', resized_img.size[0])
            setattr(picture, key + '_height', resized_img.size[1])
            save_img(resized_img, obj['folder'], filename)
    setattr(picture, 'og_width', img.size[0])
    setattr(picture, 'og_height', img.size[1])
    save_img(img, obj['folder'], filename)
    picture.save()
    return picture
