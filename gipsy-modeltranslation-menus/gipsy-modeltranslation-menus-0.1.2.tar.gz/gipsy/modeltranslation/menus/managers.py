#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from modeltranslation.manager import MultilingualManager

from gipsy.menus.managers import MenuNodeManager as MenuNodeManagerBase


class MenuNodeManager(MenuNodeManagerBase, MultilingualManager):
    pass
