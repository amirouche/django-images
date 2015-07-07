from django.contrib import admin

from .models import Image


def size_display_factory(size):
    """Create a function to use an a model field display in the admin list"""
    def getter(model):
        infos = getattr(model, size)
        html = '<a href="%s">%s</a>'
        label = '%sx%s' % (infos['width'], infos['height'])
        html = html % (
            model.url(size),
            label
        )
        return html
    getter.__name__ = size
    getter.allow_tags = True
    getter.short_description = size
    return getter


class ImageAdmin(admin.ModelAdmin):
    """Custom admin for Image model"""

    list_display = ['preview', 'name', 'xs', 'sm', 'md', 'lg', 'og']

    def __init__(self, *args, **kwargs):
        for size in ['xs', 'sm', 'md', 'lg', 'og']:
            setattr(self, size, size_display_factory(size))

        super(ImageAdmin, self).__init__(*args, **kwargs)

    def preview(self, model):
        """Display the image in the smallest size"""
        html = '<img src="%s" alt="%s"/>' % (
            model.xs['url'],
            model.name
        )
        return html
    preview.allow_tags = True

admin.register(Image)(ImageAdmin)
