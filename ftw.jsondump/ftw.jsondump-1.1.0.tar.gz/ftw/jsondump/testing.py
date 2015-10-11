from ftw.builder.testing import BUILDER_LAYER
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.configuration import xmlconfig
import ftw.jsondump.tests.builders


class FtwJsondumpLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'

            '  <include package="ftw.jsondump.tests" file="tests.zcml" />'
            '</configure>',
            context=configurationContext)

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        applyProfile(portal, 'ftw.jsondump.tests:integration')


FTW_JSONDUMP_FIXTURE = FtwJsondumpLayer()
FTW_JSONDUMP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_JSONDUMP_FIXTURE,), name="FtwJsondump:Integration")
