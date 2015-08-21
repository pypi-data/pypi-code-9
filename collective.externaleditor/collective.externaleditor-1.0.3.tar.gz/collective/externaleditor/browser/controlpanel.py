# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.externaleditor import ExternalEditorMessageFactory as _
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from zope.component import adapts
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import implements
from zope.schema import Bool
from zope.schema import Choice
from zope.schema import List


class IExternalEditorSchema(Interface):

    ext_editor = Bool(
        title=_(u"label_externaleditor_enabled",
                default=u"Enable External Editor feature"),
        description=_(u"help_externaleditor_enabled",
                      default=u"Determines if the External Editor feature "
                              "is enabled. This feature requires a special "
                              "client-side application installed. The users "
                              "also have to enable this in their "
                              "preferences."),
        default=True,
        required=False,
    )

    externaleditor_enabled_types = List(
        title=_(u"label_externaleditor_enabled_types",
                default=u"Content types editable with External Editor"),
        required=False,
        default=['File', 'Image', ],
        description=_(u"help_externaleditor_enabled_types",
                      default=u"Choose here the content types where the "
                              "External Editor action will be available"),
        value_type=Choice(
            title=u"externaleditor_enabled_types",
            source="plone.app.vocabularies.ReallyUserFriendlyTypes"),
    )


class ExternalEditorControlPanelForm(controlpanel.RegistryEditForm):

    id = 'LanguageControlPanel'
    label = _('External Editor settings')
    description = _('External Editor settings')
    schema = IExternalEditorSchema
    schema_prefix = 'externaleditor'


class ExternalEditorControlPanel(controlpanel.ControlPanelFormWrapper):

    form = ExternalEditorControlPanelForm
