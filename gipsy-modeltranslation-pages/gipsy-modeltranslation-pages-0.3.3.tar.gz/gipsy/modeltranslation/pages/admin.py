#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
This module does that.
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from django.contrib import admin
# from modeltranslation.admin import TranslationAdmin

from gipsy.modeltranslation.pages.forms import PageAdminForm
from gipsy.modeltranslation.pages.models import Page
from gipsy.pages.admin_base import PageAdminBase

from django.conf import settings

if 'gipsy.modeltranslation.sections' in settings.INSTALLED_APPS:
    from gipsy.modeltranslation.sections.admin import SectionInlineAdmin
else:
    from gipsy.sections.admin import SectionInlineAdmin


# FIXME: turned of for now - until we write js for switching fields
# class PageAdmin(TranslationAdmin, PageAdminBase):
class PageAdmin(PageAdminBase):
    add_form = PageAdminForm
    form = PageAdminForm
    inlines = [SectionInlineAdmin]

    # no idea why its not working with TranslationAdmin
    date_hierarchy = None

    def _create_formsets(self, request, obj, change):
        "Override to not display inlines in add_view."
        if not change:
            self.inlines = []
        return super(PageAdmin, self)._create_formsets(request, obj, change)

    # FIXME: turned of for now - until we write js for switching fields
    # def get_fieldsets(self, request, obj=None):
    #     if obj is None:
    #         return self._patch_fieldsets(self.add_fieldsets)
    #     return super(PageAdmin, self).get_fieldsets(request, obj=obj)


admin.site.register(Page, PageAdmin)
