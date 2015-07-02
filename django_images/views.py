# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils.text import slugify
from django.http import HttpResponseRedirect

from .pictt import save
from .models import Picture
from .forms import PictureForm


def debug(request):
    form = PictureForm()
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            filename = slugify(data['name'])
            save(
                data['picture'],
                filename,
                data['ptype']
            )
            return HttpResponseRedirect('/')
    pictures = Picture.objects.all()
    return render(request, 'django_images.html', {
        'form': form,
        'pictures': pictures,
    })
