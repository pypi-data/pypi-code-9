# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('favman.views',
    url(r'^toggle/$', 'toggle_favorite', name='favman_toggle'),
    url(r'^list/$', 'list_favorites', name='favman_list'),
)

