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
"""Interface definitions."""

# zope imports
from zope import schema
from zope.interface import Interface

# local imports
from themes.realestate_ecuador.i18n import _


class IMLSEcuadorSettings(Interface):
    """Registry settings for themes.realestate_ecuador.
    This records stored in the configuration registry and obtainable
    via plone.registry.
    """

    theme_color = schema.Choice(
        title=_(u"Choose the color of the theme"),
        values =['green', 'red', 'blue', 'yellow', 'random', 'deactivate']
        )

    show_recent_listings = schema.Bool(
        default=True,
        required=True,
        title=_(
            u"label_show_recent_listings",
            default=u"Show 'Latest Listings' on Frontpage",
        ),
    )

    recent_listings_count = schema.Int(
        default=3,
        required=True,
        title=_(
            u"label_recent_listings_count",
            default=u"Number of 'Latest Listings' to display",
        ),
    )

    recent_listings_url_en = schema.TextLine(
        default=u"latest-listings",
        required=False,
        title=_(
            u"label_recent_listings_url_en",
            default=u"'Latest Listings' URL (English)",
        ),
    )

    heading_latest_listings_en = schema.TextLine(
        default=u"Latest Listings",
        required=True,
        title=_(
            u"label_heading_latest_listings_en",
            default=u"Heading 'Latest Listings' (English)",
        ),
    )

    recent_listings_url_es = schema.TextLine(
        default=u"ultimas-listados",
        required=False,
        title=_(
            u"label_recent_listings_url_es",
            default=u"'Latest Listings' URL (Spanish)",
        ),
    )

    heading_latest_listings_es = schema.TextLine(
        default=u"Ultimas Listados",
        required=True,
        title=_(
            u"label_heading_latest_listings_es",
            default=u"Heading 'Latest Listings' (Spanish)",
        ),
    )

    show_pop_search = schema.Bool(
        default=True,
        required=True,
        title=_(
            u"label_show_pop_search",
            default=u"Show 'Popular Searches' on Frontpage",
        ),
    )

    heading_pop_searches_en = schema.TextLine(
        default=u"Popular Searches",
        required=True,
        title=_(
            u"label_heading_pop_searches_en",
            default=u"Heading 'Popular Searches' (English)",
        ),
    )

    pop_search_folder_en = schema.TextLine(
        default=u"popular-searches",
        required=False,
        title=_(
            u"label_pop_search_folder_en",
            default=u"Folder with the 'Popular Searches' Collections (English)",
        ),
    )

    heading_pop_searches_es = schema.TextLine(
        default=u"Búsquedas más populares",
        required=True,
        title=_(
            u"label_heading_pop_searches_es",
            default=u"Heading 'Popular Searches' (Spanish)",
        ),
    )

    pop_search_folder_es = schema.TextLine(
        default=u"busquedas-mas-populares",
        required=False,
        title=_(
            u"label_pop_search_folder_es",
            default=u"Folder with the 'Popular Searches' Collections (Spanish)",
        ),
    )