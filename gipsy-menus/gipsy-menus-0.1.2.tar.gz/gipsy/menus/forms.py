#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
This module does that.
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from gipsy.menus.models import MenuNode
from gipsy.menus.forms_base import MenuNodeAdminFormBase


class MenuNodeAdminForm(MenuNodeAdminFormBase):

    class Meta:
        model = MenuNode
        fields = '__all__'
