#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

from gipsy.menus.models_base import MenuNodeAbstract
from gipsy.modeltranslation.menus.managers import MenuNodeManager


class MenuNode(MenuNodeAbstract):

    objects = MenuNodeManager()
