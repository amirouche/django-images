# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils.text import slugify
from django.http import HttpResponseRedirect

from django_images.pictt import save
from django_images.models import Picture
from django_images.forms import PictureForm
from django_images.forms import PictureFixedFormatForm


def index(request):
    """Display the list of pictures in all sizes"""
    pictures = Picture.objects.all()
    return render(request, 'index.html', {
        'pictures': pictures,
    })


def generic(request):
    """Submit picture using form with format choice"""
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
    else:
        form = PictureForm()
    return render(request, 'django_images.html', {
        'form': form,
    })


def fixed(request):
    """Submit picture using fixed format form"""
    if request.method == 'POST':
        form = PictureFixedFormatForm(
            '1',
            'cover example',
            request.POST,
            request.FILES
        )
        if form.is_valid():
            picture = form.cleaned_data['picture']
            filename = slugify(form.name)
            save(
                picture,
                filename,
                form.ptype,
            )
            return HttpResponseRedirect('/')
    else:
        form = PictureFixedFormatForm(
            '1',
            'cover example',
        )
    return render(request, 'django_images.html', {
        'form': form,
    })
