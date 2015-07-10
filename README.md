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

The proxy model allows to do two things:

- Specify how an image will be resized by [python-image-resize](https://github.com/VingtCinq/python-resize-image).
- Which folder the image will be stored in. In this example images will be stored in `BackgroundImage` folder.

In the view you have to:

- Use `django_images.forms.ImageForm(specs, post, files)` to validate images. `ImageForm` will make sure that the image can be resized by *python-image-resize* and saved as the given proxy `Image` model.
- Use `Image.create(image, name)` to save it with the the  proxy model you want the image to be associated with, in this case it's `BackgroundImage.create` that must be called.

```python
def add(request):
    """Submit image using form"""
    if request.method == 'POST':
        # Create form to validate the image
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

Once you have created a few images, you can access them using their `Image` proxy model, for instance the following code:

```python
background = BackgroundImage.objects.all()[0]
print(background.all())
```

Will return something like:

```python
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

You can access this data size by size using ``backgroudn.xs``, ``background.lg`` and so on...

`url` field is computed dynamically using `IMAGES_URL` or `MEDIA_URL` django settings.

The gist of this application is the ability to create images with size fine-tuned for your (bootstrap) template
without having to worry about the code behind it. Pass the image instance to the template and depending
on the context you can use the appropriate image size, for instance the following code will display
the medium image size of `background`:

```html
<img src="{{ background.md.url }}" width="{{ background.md.width }}" heigth="{{ background.md.heigth }}" />
```

Don't forget to have a look at the example project!
