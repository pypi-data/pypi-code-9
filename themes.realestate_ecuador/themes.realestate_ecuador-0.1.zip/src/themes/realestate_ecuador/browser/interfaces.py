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
"""Interface definitions for browser related things."""

# zope imports
from plone.theme.interfaces import IDefaultPloneLayer
from Products.ATContentTypes.interfaces.image import IATImage
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from zope.interface import Interface


class ICustomerSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""

class ICarouselImage(IATImage):
    """Marker interface to override collective.carousels default view"""

class ICarouselMarker(IATContentType):
    """Marker interface to override collective.carousels default view"""

class IFrontPage(Interface):
    """Marker interface for the custom front page."""
