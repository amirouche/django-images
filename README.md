# django-images

A simple django app to upload images, resize them and save them into s3 via django-storages.

## Usage

To make use of django images you only need to setup a view with the following code:

```python
from django.shortcuts import render
from django.utils.text import slugify
from django.http import HttpResponseRedirect

from django_images.pictt import save
from django_images.models import Picture
from django_images.forms import PictureForm


def resize(request):
    form = PictureForm()
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            filename = slugify(data['name'])
            save(data['picture'], filename, data['ptype'])
            return HttpResponseRedirect('/')
    return render(request, resize.html', {'form': form})
```

This view will show a form to resize images based on the specifications. You can customize the form and the methods
used to resize images by defining `PICTURES_FORMATS`, a default value exist in `django_images.settings`. Here is another example:

```python
DEFAULT_PICTURE_FORMATS = {
    "1": {
        "folder": "covers",
        "display": "Background image",
        "sizes": {
            "xs": {"size": [105, 69], "method": "cover"},
            "sm": {"size": [350, 230], "method": "cover"},
            ...
        }
    },
    "2": {
        "folder": "content",
        "display": "Content image",
        "sizes": {
            "xs": {"size": 50, "method": "width"},
            "sm": {"size": 120, "method": "width"},
            ...
        }
    }
}
```

Once you have created a few pictures, you can access them using `Picture` model:

```
>>> from django_images.models import Picture
>>> Picture.objects.all()
[<Picture: spam>, <Picture: egg>, <Picture: beer>, <Picture: monkey>, <Picture: sky>, , <Picture: earth>]
```

Pass the picture instance to the template and depending on your need you can access the appropriate image
size, for instance the following code will display the medium image size of `picture`:

```html
<img src="{{ picture.md.url }}" width="{{ picture.md.width }}" heigth="{{ picture.md.heigth }}" />
```
