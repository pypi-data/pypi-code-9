#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
This module does that.
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from gipsy.modeltranslation.pages.forms import PageAdminForm
from gipsy.modeltranslation.pages.models import Page
from gipsy.pages.admin_base import PageAdminBase

from django.conf import settings

if 'gipsy.modeltranslation.sections' in settings.INSTALLED_APPS:
    from gipsy.modeltranslation.sections.admin import SectionInlineAdmin
else:
    from gipsy.sections.admin import SectionInlineAdmin


class PageAdmin(PageAdminBase, TranslationAdmin):
    form = PageAdminForm
    inlines = [SectionInlineAdmin]

    # no idea why its not working with TranslationAdmin
    date_hierarchy = None


admin.site.register(Page, PageAdmin)
