from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from gallery.views import add
from gallery.views import add_multiformats
from gallery.views import index


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^add/$', add),
    url('^add-multiformats/$', add_multiformats),
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
