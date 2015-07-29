#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from gipsy.modeltranslation.pages.managers import PageManager
from gipsy.pages.models_base import PageBase
from django.conf import settings

if 'gipsy.modeltranslation.sections' in settings.INSTALLED_APPS:
    from gipsy.modeltranslation.sections.managers import SectionsManager
else:
    from gipsy.sections.managers import SectionsManager


class Page(PageBase):

    objects = PageManager()
    sections = SectionsManager()
