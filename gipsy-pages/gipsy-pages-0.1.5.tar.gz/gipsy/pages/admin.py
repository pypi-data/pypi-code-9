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
    form = PageAdminForm
    inlines = [SectionInlineAdmin]


admin.site.register(Page, PageAdmin)
