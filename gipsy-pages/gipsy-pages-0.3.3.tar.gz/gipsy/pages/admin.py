#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
This module does that.
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from django.contrib import admin

from gipsy.pages.admin_base import PageAdminBase
from gipsy.pages.forms import PageAdminForm
from gipsy.pages.models import Page
from gipsy.sections.admin import SectionInlineAdmin


class PageAdmin(PageAdminBase):
    add_form = PageAdminForm
    form = PageAdminForm
    inlines = [SectionInlineAdmin]

    def _create_formsets(self, request, obj, change):
        "Override to not display inlines in add_view."
        if not change:
            self.inlines = []
        return super(PageAdmin, self)._create_formsets(request, obj, change)


admin.site.register(Page, PageAdmin)
