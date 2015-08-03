# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('gsschema.views',
    url(r'^$', 'index', name='index'),
    url(r'download', 'download', name='download'),
    url(r'describe', 'describe', name='describe'),
    url(r'upload', 'upload', name='upload'),
)
