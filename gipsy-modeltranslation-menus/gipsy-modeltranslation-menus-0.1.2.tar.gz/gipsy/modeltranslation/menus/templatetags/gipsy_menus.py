#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
This module does that.
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from django import template

from gipsy.modeltranslation.menus.models import MenuNode
from gipsy.menus.templatetags.gipsy_menus_base import menu_tag


register = template.Library()


@register.tag
def menu(parser, token):
    return menu_tag(MenuNode, parser, token)
menu.__doc__ = menu_tag.__doc__
