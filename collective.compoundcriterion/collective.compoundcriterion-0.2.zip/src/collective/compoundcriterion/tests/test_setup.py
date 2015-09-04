# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.compoundcriterion.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of collective.compoundcriterion into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.compoundcriterion is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.compoundcriterion'))

    def test_uninstall(self):
        """Test if collective.compoundcriterion is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.compoundcriterion'])
        self.assertFalse(self.installer.isProductInstalled('collective.compoundcriterion'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveCompoundcriterionLayer is registered."""
        from collective.compoundcriterion.interfaces import ICollectiveCompoundcriterionLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveCompoundcriterionLayer, utils.registered_layers())
