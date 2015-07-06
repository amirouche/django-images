# -*- coding: utf-8 -*-
from PIL import Image
from django import forms

from resizeimage import resizeimage
from resizeimage.imageexceptions import ImageSizeError

from .models import PICTURE_CHOICES
from .settings import PICTURE_FORMATS


def validate(picture, ptype):
    # compute max constraint size with method
    formats = PICTURE_FORMATS[ptype]
    maximum = formats['sizes'].values()[0]['size']
    method = formats['sizes'].values()[0]['method']
    for value in formats['sizes'].values()[1:]:
        size = max(maximum, value['size'])
        if size != maximum:
            method = value['method']
            maximum = size
    method = 'resize_' + method
    method = getattr(resizeimage, method)

    # mock close method so that PIL doesn't really close picture
    close_method = picture.close
    picture.close = lambda *args, **kwargs: None
    try:
        # do validation against the max constraint
        with Image.open(picture) as image:
            method.validate(image, maximum)
    except ImageSizeError as exc:
        # the image doesn't satisfy the constraint.
        return False, exc.message
    else:
        # It's ok, reset picture position and close method
        picture.file.seek(0)
        picture.close = close_method
        return True, None


class PictureForm(forms.Form):
    """Validate that the given picture can be resized"""
    
    picture = forms.FileField()
    ptype = forms.ChoiceField(
        choices=PICTURE_CHOICES,
        label=u"Type de photo"
    )
    name = forms.CharField()

    def is_valid(self):
        if not super(PictureForm, self).is_valid():
            return False
        else:
            data = self.clean()
            picture = data['picture']
            ptype = data['ptype']
            ok, message = validate(picture, str(ptype))
            if ok:
                return True
            else:
                self.add_error('picture', message)


class PictureFixedFormatForm(forms.Form):
    """Same as `PictureForm` except that the picture format is fixed"""

    picture = forms.FileField()

    def __init__(self, ptype, name, *args, **kwargs):
        self.ptype = ptype
        self.name = name
        super(PictureFixedFormatForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        if not super(PictureFixedFormatForm, self).is_valid():
            return False
        else:
            picture = self.clean()['picture']
            ptype = self.ptype
            ok, message = validate(picture, str(ptype))
            if ok:
                return True
            else:
                self.add_error('picture', message)
