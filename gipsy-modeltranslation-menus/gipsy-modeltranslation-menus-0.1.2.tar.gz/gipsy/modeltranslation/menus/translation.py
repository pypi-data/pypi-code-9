#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
Register translations
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from modeltranslation.translator import translator, TranslationOptions
from gipsy.modeltranslation.menus.models import MenuNode


class MenuNodeTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'description', 'options', 'url')

translator.register(MenuNode, MenuNodeTranslationOptions)
