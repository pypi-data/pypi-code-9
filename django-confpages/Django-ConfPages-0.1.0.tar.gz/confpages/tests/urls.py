from __future__ import absolute_import

from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
    url(r'^p/', include('confpages.urls')),
)
