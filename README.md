# django-images

A simple django app to upload images, resize them and save them into s3 via django storage facility.

## Dependencies

- Pillow 2.7++
- Python 2.7/3.4
- [python-image-resize](https://github.com/VingtCinq/python-resize-image) 1.1.3++

## Usage

To make use of django images you need to setup a **proxy model** like the following:

```python
from django_images.models import Image
from django_images.models import Specification


class BackgroundImage(Image):

    class Meta:
        proxy = True

    xs = Specification(method='width', size=100)
    sm = Specification(method='width', size=300)
    md = Specification(method='width', size=600)
    lg = Specification(method='width', size=1000)

```

This specify how an image will be resized by [python-image-resize](https://github.com/VingtCinq/python-resize-image).

Inside your view you have to use `django_images.forms.ImageForm` to validate an image before saving it with the the proxy model you want the image to be associated with, in this case `BackgroudnImage.create`:

```python
def add(request):
    """Submit image using form"""
    if request.method == 'POST':
        # Create form for validating this image
        form = ImageForm(BackgroundImage.specs(), request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            # Image is valid for the resize, save that image in storage and cache
            # its infos in the database
            BackgroundImage.create(data['image'])
            return redirect('/')
        else:
        # Create an empty form
        form = ImageForm(BackgroundImage.specs())
    return render(request, 'django_images.html', dict(form=form))
```

Once you have created a few pictures, you can access them using `Picture` model, for instance the following code:

```python
background = BackgroundImage.objects.all().all()[0]
```

Will return:

```python
{
    'og': {
        u'url': u'/media/1001142f313e40bbb4ad2490d1ffbaef.jpeg',
        u'width': 5760,
        u'heigth': 3840,
        u'filepath': u'1001142f313e40bbb4ad2490d1ffbaef.jpeg'
    },
    'xs': {
        u'url': u'/media/1001142f313e40bbb4ad2490d1ffbaef_xs.jpeg',
        u'width': 100,
        u'heigth': 66,
        u'filepath': u'1001142f313e40bbb4ad2490d1ffbaef_xs.jpeg'
    },
    'lg': {
        u'url': u'/media/1001142f313e40bbb4ad2490d1ffbaef_lg.jpeg',
        u'width': 1000,
        u'heigth': 666,
        u'filepath': u'1001142f313e40bbb4ad2490d1ffbaef_lg.jpeg'
    },
    'sm': {
        u'url': u'/media/1001142f313e40bbb4ad2490d1ffbaef_sm.jpeg',
        u'width': 300,
        u'heigth': 200,
        u'filepath': u'1001142f313e40bbb4ad2490d1ffbaef_sm.jpeg'
    },
    'md': {
        u'url': u'/media/1001142f313e40bbb4ad2490d1ffbaef_md.jpeg',
        u'width': 600,
        u'heigth': 400,
        u'filepath': u'1001142f313e40bbb4ad2490d1ffbaef_md.jpeg'
    }
}

```

You can access this data size by size using ``backgroudn.xs``, ``background.lg`` and so on...

The gist of this application is the ability to create images with size fine-tuned for your (bootstrap) template
without having to worry about the code behind it. Pass the image instance to the template and depending
on the context you can use the appropriate image size, for instance the following code will display
the medium image size of `background`:

```html
<img src="{{ background.md.url }}" width="{{ background.md.width }}" heigth="{{ background.md.heigth }}" />
```

Don't forget to have a look at the example project!
