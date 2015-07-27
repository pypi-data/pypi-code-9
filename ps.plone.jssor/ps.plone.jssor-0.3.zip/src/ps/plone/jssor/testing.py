# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig

import ps.plone.jssor


class PsPloneJssorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            ps.plone.jssor,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ps.plone.jssor:default')


PS_PLONE_JSSOR_FIXTURE = PsPloneJssorLayer()


PS_PLONE_JSSOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PS_PLONE_JSSOR_FIXTURE,),
    name='PsPloneJssorLayer:IntegrationTesting'
)


PS_PLONE_JSSOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PS_PLONE_JSSOR_FIXTURE,),
    name='PsPloneJssorLayer:FunctionalTesting'
)


PS_PLONE_JSSOR_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PS_PLONE_JSSOR_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PsPloneJssorLayer:AcceptanceTesting'
)
