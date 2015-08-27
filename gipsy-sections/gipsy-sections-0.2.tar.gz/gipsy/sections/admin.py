#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib import admin

from gipsy.sections.admin_base import SectionAdminBase, SectionInlineAdminBase
from gipsy.sections.forms import SectionAdminForm
from gipsy.sections.models import Section


class SectionInlineInlineAdmin(SectionInlineAdminBase):
    model = Section
    form = SectionAdminForm


class SectionInlineAdmin(SectionInlineAdminBase):
    model = Section
    form = SectionAdminForm
    inlines = [SectionInlineInlineAdmin]


class SectionAdmin(SectionAdminBase):
    form = SectionAdminForm
    inlines = [SectionInlineAdmin]


admin.site.register(Section, SectionAdmin)
