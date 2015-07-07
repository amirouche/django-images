# -*- coding: utf-8 -*-
import sys

from PIL import Image
from django import forms

from resizeimage import resizeimage
from resizeimage.imageexceptions import ImageSizeError

from .models import IMAGE_CHOICES
from .settings import IMAGE_FORMATS


if sys.version_info > (3, 0):
    PY3 = True
else:
    PY3 = False


def validate(image, ptype):
    # compute max constraint size with method
    formats = IMAGE_FORMATS[ptype]
    maximum = list(formats['sizes'].values())[0]['size']
    method = list(formats['sizes'].values())[0]['method']
    for value in list(formats['sizes'].values())[1:]:
        size = max(maximum, value['size'])
        if size != maximum:
            method = value['method']
            maximum = size
    method = 'resize_' + method
    method = getattr(resizeimage, method)

    # XXX: monkey patch close method
    # so that PIL doesn't really close the file
    # XXX: with Python 2 we can do this on `image`
    # but because of the new behavior of str/bytes
    # in python 3 we use the raw fd
    if PY3:
        try:
            fd = image.file.file.raw
        except AttributeError:
            # During tests file is backed by a buffer
            fd = image.file.buffer.raw
    else:
        fd = image
    close_method = fd.close
    fd.close = lambda *args, **kwargs: None
    try:
        # do validation against the max constraint
        with Image.open(fd) as pil_image:
            method.validate(pil_image, maximum)
    except ImageSizeError as exc:
        # the image doesn't satisfy the constraint.
        return False, exc.message
    else:
        # XXX: It's ok, reset image position and close method
        fd.seek(0)
        fd.close = close_method
        return True, None


class ImageForm(forms.Form):
    """Validate that the given image can be resized"""

    image = forms.FileField()
    ptype = forms.ChoiceField(
        choices=IMAGE_CHOICES,
        label=u"Type de photo"
    )
    name = forms.CharField()

    def is_valid(self):
        if not super(ImageForm, self).is_valid():
            return False
        else:
            data = self.clean()
            image = data['image']
            ptype = data['ptype']
            ok, message = validate(image, str(ptype))
            if ok:
                return True
            else:
                self.add_error('image', message)


class ImageFixedFormatForm(forms.Form):
    """Same as `ImageForm` except that the image format is fixed"""

    image = forms.FileField()

    def __init__(self, ptype, name, *args, **kwargs):
        self.ptype = ptype
        self.name = name
        super(ImageFixedFormatForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        if not super(ImageFixedFormatForm, self).is_valid():
            return False
        else:
            image = self.clean()['image']
            ptype = self.ptype
            ok, message = validate(image, str(ptype))
            if ok:
                return True
            else:
                self.add_error('image', message)
