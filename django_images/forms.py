# -*- coding: utf-8 -*-
import sys

from PIL import Image
from django import forms

if sys.version_info > (3, 0):
    PY3 = True
else:
    PY3 = False


class ImageForm(forms.Form):
    """Validate that the given image can be resized"""

    image = forms.FileField()
    name = forms.CharField()

    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(ImageForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        specs = self.model.specs()
        if not super(ImageForm, self).is_valid():
            return False
        else:
            data = self.clean()
            image = data['image']

            # compute max constraint size with method
            widths = [0]
            heights = [0]
            for value in specs:
                if value.method in ('contain', 'thumbnail'):
                    pass  # no constraint
                elif value.method == 'cover':
                    widths.append(value.size[0])
                    heights.append(value.size[1])
                elif value.method == 'width':
                    widths.append(value.size)
                elif value.method == 'height':
                    heights.append(value.size)
                elif value.method == 'crop':
                    widths.append(value.size[0])
                    heights.append(value.size[1])

            constraint = (max(widths), max(heights))

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
            # check constraint
            image = Image.open(fd)
            if constraint > image.size:
                msg = 'Image is too small, Image size : %s, Required size : %s'
                msg = msg % constraint
                self.add_error('image', msg)
                return False
            else:
                # It's ok, reset image position
                fd.seek(0)
                return True

    def save(self):
        return self.model.create(**self.cleaned_data)
