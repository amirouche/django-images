# -*- coding: utf-8 -*-
from PIL import Image
from django import forms

from resizeimage import resizeimage
from resizeimage.imageexceptions import ImageSizeError

from .models import IMAGE_CHOICES
from .settings import IMAGE_FORMATS


def validate(image, ptype):
    # compute max constraint size with method
    formats = IMAGE_FORMATS[ptype]
    maximum = formats['sizes'].values()[0]['size']
    method = formats['sizes'].values()[0]['method']
    for value in formats['sizes'].values()[1:]:
        size = max(maximum, value['size'])
        if size != maximum:
            method = value['method']
            maximum = size
    method = 'resize_' + method
    method = getattr(resizeimage, method)

    # mock close method so that PIL doesn't really close image
    close_method = image.close
    image.close = lambda *args, **kwargs: None
    try:
        # do validation against the max constraint
        with Image.open(image) as pil_image:
            method.validate(pil_image, maximum)
    except ImageSizeError as exc:
        # the image doesn't satisfy the constraint.
        return False, exc.message
    else:
        # It's ok, reset image position and close method
        image.file.seek(0)
        image.close = close_method
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
