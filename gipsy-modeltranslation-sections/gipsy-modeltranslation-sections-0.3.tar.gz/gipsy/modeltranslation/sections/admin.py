#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib import admin

from gipsy.sections.admin_base import SectionAdminBase, SectionInlineAdminBase
from gipsy.modeltranslation.sections.forms import SectionAdminForm, SectionInlineAdminForm
from gipsy.modeltranslation.sections.models import Section
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline


class SectionInlineAdmin(TranslationTabularInline, SectionInlineAdminBase):
    model = Section
    add_form = SectionInlineAdminForm
    form = SectionInlineAdminForm


class SectionAdmin(TranslationAdmin, SectionAdminBase):
    group_fieldsets = True
    add_form = SectionAdminForm
    form = SectionAdminForm
    inlines = [SectionInlineAdmin]

    # no idea why its not working with TranslationAdmin
    date_hierarchy = None

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self._patch_fieldsets(self.add_fieldsets)
        return super(SectionAdmin, self).get_fieldsets(request, obj=obj)

    def _create_formsets(self, request, obj, change):
        "Override to not display inlines in add_view."
        if not change:
            self.inlines = []
        return super(SectionAdmin, self)._create_formsets(request, obj, change)


admin.site.register(Section, SectionAdmin)
