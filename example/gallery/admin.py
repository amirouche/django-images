from django.contrib import admin

from django_images.admin import ImageAdmin

from .models import BackgroundImage
from .models import Vitrine
from .models import Logo


admin.site.register(Vitrine)
admin.site.register(BackgroundImage, ImageAdmin)
admin.site.register(Logo, ImageAdmin)


