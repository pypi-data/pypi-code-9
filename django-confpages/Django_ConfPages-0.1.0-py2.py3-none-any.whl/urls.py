from __future__ import absolute_import

from django.conf.urls import patterns, url

from .views import ConfPages


urlpatterns = patterns('',
    url(r'^$', ConfPages.as_view(), {'name': 'index'}, name='confpages-index'),
    url(r'^(?P<name>\w+)/$', ConfPages.as_view(), name='confpages-detail'),
)
