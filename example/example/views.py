# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils.text import slugify
from django.http import HttpResponseRedirect

from django_images.image import save
from django_images.models import Image
from django_images.forms import ImageForm
from django_images.forms import ImageFixedFormatForm


def index(request):
    """Display the list of pictures in all sizes"""
    pictures = Image.objects.all()
    return render(request, 'index.html', {
        'pictures': pictures,
    })


def generic(request):
    """Submit image using form with format choice"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            filename = slugify(data['name'])
            save(
                data['image'],
                filename,
                data['ptype']
            )
            return HttpResponseRedirect('/')
    else:
        form = ImageForm()
    return render(request, 'django_images.html', {
        'form': form,
    })


def fixed(request):
    """Submit image using fixed format form"""
    if request.method == 'POST':
        form = ImageFixedFormatForm(
            '1',
            'cover example',
            request.POST,
            request.FILES
        )
        if form.is_valid():
            image = form.cleaned_data['image']
            filename = slugify(form.name)
            save(
                image,
                filename,
                form.ptype,
            )
            return HttpResponseRedirect('/')
    else:
        form = ImageFixedFormatForm(
            '1',
            'cover example',
        )
    return render(request, 'django_images.html', {
        'form': form,
    })
