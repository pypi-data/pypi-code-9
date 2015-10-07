# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""
from ps.plone.jssor.testing import PS_PLONE_JSSOR_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestInstall(unittest.TestCase):
    """Test installation of ps.plone.jssor into Plone."""

    layer = PS_PLONE_JSSOR_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ps.plone.jssor is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('ps.plone.jssor'))

    def test_uninstall(self):
        """Test if ps.plone.jssor is cleanly uninstalled."""
        self.installer.uninstallProducts(['ps.plone.jssor'])
        self.assertFalse(self.installer.isProductInstalled('ps.plone.jssor'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IPsPloneJssorLayer is registered."""
        from ps.plone.jssor.browser.interfaces import IJssorViewlets
        from plone.browserlayer import utils
        self.assertIn(IJssorViewlets, utils.registered_layers())
