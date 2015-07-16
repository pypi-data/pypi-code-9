##
## testing.py
##
## Copyright (C) 2013 Uli Fouquet
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""Test support/helpers for psj.policy.
"""
import unittest
from Testing.ZopeTestCase import Functional
from plone.app.testing import (
    PloneSandboxLayer, PLONE_FIXTURE, IntegrationTesting, FunctionalTesting
    )
from plone.testing import z2


class PSJPolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import psj.policy
        self.loadZCML(package=psj.policy)

        # Install product and call its initialize() function
        #z2.installProduct(app, 'psj.policy')

        # Note: you can skip this if my.product is not a Zope 2-style
        # product, i.e. it is not in the Products.* namespace and it
        # does not have a <five:registerPackage /> directive in its
        # configure.zcml.

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'psj.policy:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'psj.policy')

        # Note: Again, you can skip this if my.product is not a Zope 2-
        # style product


MY_PRODUCT_FIXTURE = PSJPolicyLayer()
MY_PRODUCT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MY_PRODUCT_FIXTURE,), name="PSJPolicy:Integration")
MY_PRODUCT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MY_PRODUCT_FIXTURE,), name="PSJPolicy:Functional")


class IntegrationTestCase(unittest.TestCase):

    layer = MY_PRODUCT_INTEGRATION_TESTING

    @property
    def portal(self):
        return self.layer['portal']


class FunctionalTestCase(Functional, unittest.TestCase):

    layer = MY_PRODUCT_FUNCTIONAL_TESTING

    @property
    def portal(self):
        return self.layer['portal']
