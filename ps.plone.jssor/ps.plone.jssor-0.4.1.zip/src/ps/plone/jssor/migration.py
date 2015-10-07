# -*- coding: utf-8 -*-
"""Migration steps for ps.plone.jssor"""

# zope imports
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import getUtility

# package namespaces
PROFILE_ID = u'profile-ps.plone.jssor'
INSTALL_PROFILE = '{0}:default'.format(PROFILE_ID)
UNINSTALL_PROFILE = '{0}:uninstall'.format(PROFILE_ID)
PROJECT_NAME = 'ps.plone.jssor'


def migrate_to_1001(context):
    """Migrate from 1000 to 1001.
    * update css
    """
    site = getUtility(IPloneSiteRoot)
    setup = getToolByName(site, 'portal_setup')
    setup.runImportStepFromProfile(INSTALL_PROFILE, 'cssregistry')
