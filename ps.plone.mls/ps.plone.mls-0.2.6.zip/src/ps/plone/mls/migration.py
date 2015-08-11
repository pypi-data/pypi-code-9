# -*- coding: utf-8 -*-
"""Migration steps for ps.plone.mls."""

# zope imports
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import getUtility

# local imports
from ps.plone.mls import config


def migrate_to_1001(context):
    """Migrate from 1000 to 1001.

    * Activate portal actions.
    """
    site = getUtility(IPloneSiteRoot)
    setup = getToolByName(site, 'portal_setup')
    setup.runImportStepFromProfile(config.INSTALL_PROFILE, 'actions')


def migrate_to_1002(context):
    """Migrate from 1001 to 1002.

    * ensure mls.css
    """
    site = getUtility(IPloneSiteRoot)
    setup = getToolByName(site, 'portal_setup')
    setup.runImportStepFromProfile(config.INSTALL_PROFILE, 'cssregistry')
    setup.runImportStepFromProfile(config.INSTALL_PROFILE, 'jsregistry')


def migrate_css(context):
    """Migrate step for simple css updates
    """
    site = getUtility(IPloneSiteRoot)
    setup = getToolByName(site, 'portal_setup')
    setup.runImportStepFromProfile(config.INSTALL_PROFILE, 'cssregistry')


def migrate_to_1005(context):
    """Migrate to 1005
    * add ps.fonts.iconmagic
    """
    site = getUtility(IPloneSiteRoot)
    quickinstaller = getToolByName(site, 'portal_quickinstaller')

    # Add ps.fonts.iconmagic
    if not quickinstaller.isProductInstalled('ps.plone.realestatefont'):
        quickinstaller.installProduct('ps.plone.realestatefont')
