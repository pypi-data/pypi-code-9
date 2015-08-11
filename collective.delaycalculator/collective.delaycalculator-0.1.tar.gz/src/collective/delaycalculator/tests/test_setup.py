# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.delaycalculator.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of collective.delaycalculator into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.delaycalculator is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.delaycalculator'))

    def test_uninstall(self):
        """Test if collective.delaycalculator is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.delaycalculator'])
        self.assertFalse(self.installer.isProductInstalled('collective.delaycalculator'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveDelaycalculatorLayer is registered."""
        from collective.delaycalculator.interfaces import ICollectiveDelaycalculatorLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveDelaycalculatorLayer, utils.registered_layers())
