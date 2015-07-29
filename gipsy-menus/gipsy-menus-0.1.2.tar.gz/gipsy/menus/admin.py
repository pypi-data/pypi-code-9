#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from django.contrib import admin
from gipsy.menus.forms import MenuNodeAdminForm
from gipsy.menus.models import MenuNode
from gipsy.menus.admin_base import MenuNodeInlineAdminBase, MenuNodeAdminBase


class MenuNodeInlineAdmin(MenuNodeInlineAdminBase):
    form = MenuNodeAdminForm
    model = MenuNode


class MenuNodeAdmin(MenuNodeAdminBase):
    form = MenuNodeAdminForm
    inlines = [MenuNodeInlineAdmin]


admin.site.register(MenuNode, MenuNodeAdmin)
