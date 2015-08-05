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
"""Realestate Ecuador Settings Control Panel."""

# zope imports
from plone.app.registry.browser import controlpanel

# local imports
from themes.realestate_ecuador.i18n import _
from themes.realestate_ecuador.interfaces import IMLSEcuadorSettings


class MLSEcuadorSettingsEditForm(controlpanel.RegistryEditForm):
    """themes.realestate_ecuador Settings Form"""

    schema = IMLSEcuadorSettings
    label = _(
        u"heading_mls_settings",
        default=u"Theme Settings for Ecuador Realestate",
    )
    description = _(
        u"help_mls_settings",
        default=u"Customize the Layout and functions of the Ecuador Realestate Theme",
    )

    def updateFields(self):
        super(MLSEcuadorSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(MLSEcuadorSettingsEditForm, self).updateWidgets()


class MLSEcuadorSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """themes.realestate_ecuador Settings Control Panel"""

    form = MLSEcuadorSettingsEditForm
