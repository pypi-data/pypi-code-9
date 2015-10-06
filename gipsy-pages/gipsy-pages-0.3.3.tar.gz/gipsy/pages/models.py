#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from gipsy.pages.managers import PageManager
from gipsy.sections.managers import SectionsManager
from gipsy.pages.models_base import PageBase


class Page(PageBase):

    objects = PageManager()
    sections = SectionsManager()
