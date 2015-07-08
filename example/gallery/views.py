# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect

from django_images.forms import ImageForm

from .models import BackgroundImage


def index(request):
    """Display the list of images in all sizes"""
    images = BackgroundImage.objects.all()
    return render(request, 'index.html', dict(images=images))


def add(request):
    """Submit image using form"""
    if request.method == 'POST':
        form = ImageForm(BackgroundImage.specs(), request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            BackgroundImage.create(data['image'])
            return redirect('/')
    else:
        form = ImageForm(BackgroundImage.specs())
    return render(request, 'django_images.html', dict(form=form))
