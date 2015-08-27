#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib import admin

from gipsy.sections.admin_base import SectionAdminBase, SectionInlineAdminBase
from gipsy.modeltranslation.sections.forms import SectionAdminForm
from gipsy.modeltranslation.sections.models import Section
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline


class SectionInlineInlineAdmin(TranslationStackedInline, SectionInlineAdminBase):
    model = Section
    form = SectionAdminForm


class SectionInlineAdmin(TranslationStackedInline, SectionInlineAdminBase):
    model = Section
    form = SectionAdminForm
    inlines = [SectionInlineInlineAdmin]


class SectionAdmin(TranslationAdmin, SectionAdminBase):
    form = SectionAdminForm
    inlines = [SectionInlineAdmin]

    # no idea why its not working with TranslationAdmin
    date_hierarchy = None


admin.site.register(Section, SectionAdmin)
