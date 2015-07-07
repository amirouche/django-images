from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from .views import generic
from .views import fixed
from .views import index


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^generic/$', generic),
    url('^fixed/$', fixed),
    url('^$', index),
) + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT,
    show_indexes=True
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
    show_indexes=True
)
