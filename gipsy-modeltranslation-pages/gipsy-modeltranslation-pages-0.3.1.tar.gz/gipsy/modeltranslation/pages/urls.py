#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    url(r'^$', 'gipsy.modeltranslation.pages.views.page_detail', {'path': ''},
        name='page_detail'),
    url(r'^(?P<path>[/\w\d_-]*){}$'.format(settings.APPEND_SLASH and '/' or ''),
        'gipsy.modeltranslation.pages.views.page_detail', name='page_detail'),
]
