# -*- coding: utf-8 -*-
from . import msgFact as _
from .interfaces import ISiteLogoSchema
from plone.app.registry.browser import controlpanel
from plone.formwidget.namedfile.widget import NamedImageFieldWidget


class SiteLogoControlPanelForm(controlpanel.RegistryEditForm):

    id = "SiteLogoControlPanel"
    label = _('label_site_logo_controlpanel', default=u"Site logo settings")
    description = _(
        'help_site_logo_controlpanel', default=u"Define a portal logo.")
    schema = ISiteLogoSchema
    schema_prefix = "plone"

    def updateFields(self):
        super(SiteLogoControlPanelForm, self).updateFields()
        self.fields['site_logo'].widgetFactory = NamedImageFieldWidget


class SiteControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SiteLogoControlPanelForm
