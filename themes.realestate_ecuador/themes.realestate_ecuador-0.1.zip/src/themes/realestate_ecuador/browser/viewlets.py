# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2013 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
###############################################################################
"""Custom viewlets for themes.realestate_ecuador"""

from plone.app.layout.viewlets.common import LogoViewlet, ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from datetime import date
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from themes.realestate_ecuador.interfaces import IMLSEcuadorSettings
from random import choice

RANDOM_THEMES = ['green', 'red', 'blue', 'yellow']


class LogoViewlet(LogoViewlet):
    index = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        super(LogoViewlet, self).update()

        registry = queryUtility(IRegistry)
        portal = self.portal_state.portal()
        bprops = portal.restrictedTraverse('base_properties', None)
        if bprops is not None:
            logoName = bprops.logoName
        else:
            logoName = 'logo.jpg'

        logoTitle = self.portal_state.portal_title()
        self.logo_tag = portal.restrictedTraverse(
            logoName).tag(title=logoTitle, alt=logoTitle)
        self.navigation_root = self.portal_state.navigation_root()
        self.navigation_root_title = self.portal_state.navigation_root_title()

        self.site_title = self.portal_state.portal_title()
        self.site_descr = getattr(self.navigation_root, "Description", None)
        self.registry_settings = registry.forInterface(IMLSEcuadorSettings, check=False)

    @property
    def getTheme(self):
        settings = self.registry_settings
        theme = getattr(settings, 'theme_color', None)
        if theme is None or theme == 'random':
            theme = choice(RANDOM_THEMES)
        return theme


class ColophonViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/colophone.pt')

    def update(self):
        super(ColophonViewlet, self).update()
        self.year = date.today().year
        registry = queryUtility(IRegistry)
        self.registry_settings = registry.forInterface(IMLSEcuadorSettings, check=False)

    @property
    def getTheme(self):
        settings = self.registry_settings
        theme = getattr(settings, 'theme_color', None)
        if theme is None or theme == 'random':
            theme = choice(RANDOM_THEMES)
        return theme

