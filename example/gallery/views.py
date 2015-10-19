# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect

from django_images.models import Image
from django_images.forms import ImageForm
from django_images.forms import MultipleFormatImageForm

from .models import BackgroundImage


def index(request):
    """Display the list of images in all sizes"""
    images = BackgroundImage.objects.all()
    return render(request, 'index.html', dict(images=images))


def add(request):
    """Submit image using form"""
    if request.method == 'POST':
        form = ImageForm(BackgroundImage, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ImageForm(BackgroundImage.specs())
    return render(request, 'django_images.html', dict(form=form))


def add_multiformats(request):
    """Submit image using form where format can be chosen"""
    if request.method == 'POST':
        form = MultipleFormatImageForm(
            Image.formats(),
            request.POST,
            request.FILES
        )
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MultipleFormatImageForm(Image.formats())
    return render(request, 'django_images.html', dict(form=form))
