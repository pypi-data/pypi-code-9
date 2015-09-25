#-*- coding: utf-8 -*-

from plone.app.registry.browser import controlpanel

from ityou.follow.interfaces import IFollowSettings, _

class FollowSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IFollowSettings
    label = _(u"Follow stettings")
    description = _(u"""Settings of the follow and like variables
    """)

    def updateFields(self):
        super(FollowSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(FollowSettingsEditForm, self).updateWidgets()

class FollowSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = FollowSettingsEditForm
