from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class ThemesRealestate_Ecuador(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import themes.realestate_ecuador
        xmlconfig.file('configure.zcml',
                       themes.realestate_ecuador,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'themes.realestate_ecuador:default')

THEMES_REALESTATE_ECUADOR_FIXTURE = ThemesRealestate_Ecuador()
THEMES_REALESTATE_ECUADOR_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(THEMES_REALESTATE_ECUADOR_FIXTURE, ),
                       name="ThemesRealestate_Ecuador:Integration")