#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from gipsy.sections.models_base import SectionBase
from gipsy.modeltranslation.sections.managers import SectionManager, SectionsManager


class Section(SectionBase):

    objects = SectionManager()
    sections = SectionsManager()
