#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
Register translations
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from modeltranslation.translator import translator, TranslationOptions
from gipsy.modeltranslation.sections.models import Section


class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'description', 'options')

translator.register(Section, SectionTranslationOptions)
