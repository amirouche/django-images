# django-images

A simple django app to upload images, resize them and save them into s3 via django storage facility.


## Dependencies

- Pillow 2.7+
- Python 2.7/3.4
- [python-image-resize](https://github.com/VingtCinq/python-resize-image) 1.1.3+


## Settings

If you use custom django storage `IMAGES_URL` must be set as the root url to serve images. If
`IMAGES_URL` is not set, it will use `MEDIA_URL`. So `ÌMAGES_URL` or `MEDIA_URL` must be set.


## Working with Amazon Storage (AWS S3)

Install [django-storages-redux](https://pypi.python.org/pypi/django-storages-redux/1.2) and
[boto](https://pypi.python.org/pypi/boto), then add `'storages'` to ``INSTALLED_APPS``. Specify
`DEFAULT_FILE_STORAGE`:

```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
```

And provide the S3 credentials:

```python
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''
```

## Usage

To make use of django images you need to setup a **proxy model** like the following:

```python
from django_images.models import Image
from django_images.models import Specification


class BackgroundImage(Image):

    class Meta:
        proxy = True

    xs = Specification(method='contain', size=(100, 100))
    sm = Specification(method='height', size=300)
    md = Specification(method='width', size=300)
    lg = Specification(method='cover', size=(1000, 1000))
```

The proxy model allows to do two things:

- Specify how an image will be resized by [python-image-resize](https://github.com/VingtCinq/python-resize-image). `size` is passed as the `size` argument of python-resize-image functions.

- Which folder the image will be stored in. In this example images will be stored in `BackgroundImage` folder.

In the view you have to:

- Use `django_images.forms.ImageForm(ImageProxyModel, post, files)` to validate images. `ImageForm` will make sure that the image can be resized by *python-image-resize* and saved as the given proxy `Image` model.

- Use `Image.create(image, name)` to save it with the proxy model you want the image to be associated with, in this case it's `BackgroundImage.create` that must be called.

```python
def add(request):
    """Submit image using form"""
    if request.method == 'POST':
        # Create form to validate the image
        form = ImageForm(BackgroundImage, request.POST, request.FILES)

        if form.is_valid():
            # Image is valid for the resize, resize it, save in storage
            # and cache its infos in the database
            image = form.save()
            return redirect('/')
        else:
        # Create an empty form
        form = ImageForm(BackgroundImage)
    return render(request, 'django_images.html', dict(form=form))
```

Once you have created a few images, you can access them using their `Image` proxy model.

Retrieve the one `BackgroundImage`:

```python
>>> backgrounds = BackgroundImage.objects.all()
>>> background = backgrounds[0]
```

Retrieve all its infos:

```python
>>> print(background.all())
{
    "og": {
        "url": "https://s3-eu-west-1.amazonaws.com/django-images/BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb.jpeg", 
        "width": 4288, 
        "heigth": 2848, 
        "filepath": "BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb.jpeg"
    }, 
    "xs": {
        "url": "https://s3-eu-west-1.amazonaws.com/django-images/BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb_xs.jpeg", 
        "width": 100, 
        "heigth": 66, 
        "filepath": "BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb_xs.jpeg"
    }, 
    "lg": {
        "url": "https://s3-eu-west-1.amazonaws.com/django-images/BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb_lg.jpeg", 
        "width": 400, 
        "heigth": 265, 
        "filepath": "BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb_lg.jpeg"
    }, 
    "sm": {
        "url": "https://s3-eu-west-1.amazonaws.com/django-images/BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb_sm.jpeg", 
        "width": 200, 
        "heigth": 132, 
        "filepath": "BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb_sm.jpeg"
    }, 
    "md": {
        "url": "https://s3-eu-west-1.amazonaws.com/django-images/BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb_md.jpeg", 
        "width": 300, 
        "heigth": 199, 
        "filepath": "BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb_md.jpeg"
    }
}
```

You can access this data size by size using ``backgroudn.xs``, ``background.md`` and so on... `background.og` is the info for
the original image file, for instance:

```python
>>> background.og
{
    "url": "https://s3-eu-west-1.amazonaws.com/django-images/BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb.jpeg", 
    "width": 4288, 
    "heigth": 2848, 
    "filepath": "BackgroundImage/beach-de3ce50519e241fb9696631727eff8cb.jpeg"
}
```

`url` field is computed dynamically using `IMAGES_URL` or `MEDIA_URL` django settings.

The gist of this application is the ability to create images with size fine-tuned for your (bootstrap) template
without having to worry about the code behind it. Pass the image instance to the template and depending
on the context you can use the appropriate image size, for instance the following code will display
the medium image size of `background`:

```html
<img src="{{ background.md.url }}" width="{{ background.md.width }}" heigth="{{ background.md.heigth }}" />
```

Don't forget to have a look at the example project!
