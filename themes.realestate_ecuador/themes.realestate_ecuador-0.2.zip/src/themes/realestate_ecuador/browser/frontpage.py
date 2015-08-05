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
"""Custom front page view for themes.realstate_ecuador"""

# zope imports
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.interface import implements
from zope.publisher.browser import BrowserView


# local imports
from themes.realestate_ecuador.interfaces import IMLSEcuadorSettings
from themes.realestate_ecuador.browser.interfaces import IFrontPage
from plone.mls.listing.api import recent_listings

HEADINGS = ['heading_latest_listings', 'heading_pop_searches']
LANGUAGES = ['en', 'es']

class FrontPageView(BrowserView):
    """Custom front page view."""
    implements(IFrontPage)

    def __call__(self):
        """Update the view and return the template."""
        self.update()
        return self.index()

    
    @property
    def catalog(self):
        context = aq_inner(self.context)
        return getToolByName(context, 'portal_catalog')

    def update(self):
        """Update the view and collect the data."""
        registry = queryUtility(IRegistry)
        self.portal_state = self.context.unrestrictedTraverse(
            "@@plone_portal_state")
        self.navigation_root_path = self.portal_state.navigation_root_path()
        self.navigation_root_url = self.portal_state.navigation_root_url()
        self.registry_settings = registry.forInterface(IMLSEcuadorSettings, check=False)
        self.lang = self.portal_state.language()
        self.headings = self._get_headings(self.lang)
        self.pop_search_folder = self._pop_search_folder
        self.pop_search_sections = self._set_pop_searches()
        self.pop_search_obj = self._set_pop_search_obj()


    def _get_headings(self, lang='en'):
        """Get the section headings dependend on the language."""
        headings = {}
        settings = self.registry_settings
        # use english heading for not implemented language
        if lang not in LANGUAGES:
            lang='en'

        for heading in HEADINGS:
            try:
                label = getattr(settings, heading + '_' + lang)
            except AttributeError:
                label = u''
            headings.update({
                heading: label,
            })
        return headings

    @property
    def recent_listings(self):
        settings = self.registry_settings
        limit = getattr(settings, 'recent_listings_count', 3)
        # TODO: Get recent listings config from references content element
        # config = ...
        params = {
            'limit': limit,
            'offset': 0,
            'lang': self.lang,
        }
        rl = recent_listings(params, batching=False)
        return rl

    @property
    def recent_listings_available(self):
        settings = self.registry_settings
        if not getattr(settings, 'show_recent_listings', True):
            return False
        return len(self.recent_listings) > 0

    @property
    def recent_listings_url(self):
        settings = self.registry_settings
        url = getattr(settings, 'recent_listings_url_' + self.lang, None)
        if url is None:
            url = ''
        return self.navigation_root_url + '/' + url

    @property
    def pop_search_available(self):
        settings = self.registry_settings
        if not getattr(settings, 'show_pop_search', True):
            return False
        return True

    @property
    def _pop_search_folder(self):
        settings = self.registry_settings
        lang='en'
        if self.lang in LANGUAGES:
            lang=self.lang

        path = self.navigation_root_path + '/' + getattr(settings, 'pop_search_folder_' + lang, None)
        return path

    @memoize
    def _set_pop_searches(self):
        """Get the Popular Search Collections."""
        path = self.pop_search_folder
        return self.catalog(portal_type='Topic',path=path,sort_on='getObjPositionInParent',)

    @memoize
    def _set_pop_search_obj(self):
        """Get the Popular Search Collection Objects."""
        object_list=[]

        for b in self.pop_search_sections:
            b_ob = b.getObject()
            foo = {'brain': b, 'results': b_ob.queryCatalog({'query': b.getPath(), 'depth': 1})}
            object_list.append(foo)

        return object_list

    def debug_me(self):
        import pdb
        from pprint import pprint
        pdb.set_trace()
