#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib import admin

from gipsy.sections.admin_base import SectionAdminBase, SectionInlineAdminBase
from gipsy.sections.forms import SectionAdminForm, SectionInlineAdminForm
from gipsy.sections.models import Section


class SectionInlineAdmin(SectionInlineAdminBase):
    model = Section
    add_form = SectionInlineAdminForm
    form = SectionInlineAdminForm


class SectionAdmin(SectionAdminBase):
    add_form = SectionAdminForm
    form = SectionAdminForm
    inlines = [SectionInlineAdmin]

    def _create_formsets(self, request, obj, change):
        "Override to not display inlines in add_view."
        if not change:
            self.inlines = []
        return super(SectionAdmin, self)._create_formsets(request, obj, change)


admin.site.register(Section, SectionAdmin)
