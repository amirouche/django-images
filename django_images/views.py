# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import PictureForm
from .models import Picture


def debug(request):
    form = PictureForm()
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect('/')
    pictures = Picture.objects.all()
    return render(request, 'django_images.html', {
        'form': form,
        'pictures': pictures,
    })
