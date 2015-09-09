from Products.CMFPlone.utils import getToolByName


PROFILE_ID = 'profile-collective.emailconfirmationregistration:default'


def upgrade_12(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    setup.runImportStepFromProfile(PROFILE_ID, 'controlpanel')
