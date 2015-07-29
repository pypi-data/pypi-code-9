#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib import admin
from gipsy.modeltranslation.menus.forms import MenuNodeAdminForm
from gipsy.modeltranslation.menus.models import MenuNode
from gipsy.menus.admin_base import MenuNodeInlineAdminBase, MenuNodeAdminBase
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline


class MenuNodeInlineAdmin(MenuNodeInlineAdminBase, TranslationTabularInline):
    form = MenuNodeAdminForm
    model = MenuNode


class MenuNodeAdmin(MenuNodeAdminBase, TranslationAdmin):
    form = MenuNodeAdminForm
    inlines = [MenuNodeInlineAdmin]


admin.site.register(MenuNode, MenuNodeAdmin)
