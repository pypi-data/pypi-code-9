# -*- coding: utf-8 -*-
from . import msgFact as _
from .interfaces import ISiteLogoSchema
from plone.app.registry.browser import controlpanel
from plone.formwidget.namedfile.widget import NamedImageFieldWidget


class SiteLogoControlPanelForm(controlpanel.RegistryEditForm):

    id = "SiteControlPanel"
    label = _(u"Site settings")
    description = _("Site-wide settings.")
    schema = ISiteLogoSchema
    schema_prefix = "plone"

    def updateFields(self):
        super(SiteLogoControlPanelForm, self).updateFields()
        self.fields['site_logo'].widgetFactory = NamedImageFieldWidget


class SiteControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SiteLogoControlPanelForm
