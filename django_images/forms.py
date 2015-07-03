# -*- coding: utf-8 -*-
from PIL import Image
from django import forms
from cStringIO import StringIO

from resizeimage import resizeimage

from .models import PICTURE_CHOICES
from .settings import PICTURE_FORMATS


class PictureForm(forms.Form):

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
            # compute max constraint size with method
            formats = PICTURE_FORMATS[str(data['ptype'])]
            maximum = formats['sizes'].values()[0]['size']
            method = formats['sizes'].values()[0]['method']
            for value in formats['sizes'].values()[1:]:
                size = max(maximum, value['size'])
                if size != maximum:
                    method = value['method']
                    maximum = size
            method = 'resize_' + method
            method = getattr(resizeimage, method)

            # Create a clone of the picture to use with validation
            # We need to do this because `Image.open` close the
            # `picture` file which can not be opened later
            picture = data['picture']
            clone = StringIO()
            clone.write(picture.file.read())

            try:
                # do validation against the max constraint
                with Image.open(clone) as image:
                    method.validate(image, maximum)
            except Exception as exc:
                # the image doesn't satify the constraint.
                self.add_error('picture', exc.message)
                return False
            else:
                # It's ok,  reset picture file seek position for later re-use
                picture.file.seek(0)
                return True
