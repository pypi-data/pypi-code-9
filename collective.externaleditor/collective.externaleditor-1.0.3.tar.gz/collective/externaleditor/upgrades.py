# -*- coding: utf-8 -*-
from collective.externaleditor.browser.controlpanel import \
    IExternalEditorSchema
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component.hooks import getSite

import logging
logger = logging.getLogger(__name__)
_marker = []


def migrate_to_registry(context):
    # get old settings if they exits
    portal = getSite()
    ext_editor = getattr(portal, 'ext_editor', _marker)
    externaleditor_enabled_types = getattr(
        portal, 'externaleditor_enabled_types', _marker)

    # create entries with the default settings
    context.runImportStepFromProfile(
        'profile-collective.externaleditor:default',
        'plone.app.registry')
    registry = getUtility(IRegistry)
    settings = registry.forInterface(
        IExternalEditorSchema, prefix='externaleditor')

    # set old settings
    if ext_editor is not _marker:
        settings.ext_editor = ext_editor
    if externaleditor_enabled_types is not _marker:
        settings.externaleditor_enabled_types = externaleditor_enabled_types
