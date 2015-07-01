# -*- coding: utf-8 -*-
from django import forms
from django.utils.text import slugify

from .models import PICTURE_CHOICES
from .pictt import save


class PictureForm(forms.Form):

    picture = forms.FileField(label=u"Photo")
    ptype = forms.ChoiceField(choices=PICTURE_CHOICES, label=u"Type de photo")
    name = forms.CharField(label=u"Nom")

    def clean(self):
        cleaned_data = super(PictureForm, self).clean()
        picture = cleaned_data.get('picture')
        ptype = cleaned_data.get('ptype')
        name = cleaned_data.get('name')

        if picture and ptype and name:
            filename = slugify(name)
            try:
                save(picture, filename, int(ptype))
            except Exception as e:
                error = forms.ValidationError(e.message)
                self.add_error('picture', error)


class PictureTypeForm(forms.Form):

    picture = forms.FileField(label=u"Photo")

    def __init__(self, ptype, name, *args, **kwargs):
        self.ptype = ptype
        self.name = name
        super(PictureTypeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PictureTypeForm, self).clean()
        picture = cleaned_data.get('picture')
        ptype = self.ptype
        name = self.name
        if picture and ptype and name:
            filename = slugify(name)
            try:
                pict = save(picture, filename, int(ptype))
            except Exception as e:  # FIXME: no generic exception
                error = forms.ValidationError(e.message)
                self.add_error('picture', error)
            else:
                self.pict = pict

    def get_pict(self):
        return self.pict
