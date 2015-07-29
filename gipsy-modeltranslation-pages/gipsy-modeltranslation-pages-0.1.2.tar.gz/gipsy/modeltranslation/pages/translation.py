#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
Register translations
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from modeltranslation.translator import translator, TranslationOptions
from gipsy.modeltranslation.pages.models import Page


class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'description', 'options', 'url_slug')

translator.register(Page, PageTranslationOptions)
