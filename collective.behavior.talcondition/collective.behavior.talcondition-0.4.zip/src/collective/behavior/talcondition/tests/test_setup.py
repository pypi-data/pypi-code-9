# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.behavior.talcondition.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of collective.behavior.talcondition into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.behavior.talcondition is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.behavior.talcondition'))

    def test_uninstall(self):
        """Test if collective.behavior.talcondition is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.behavior.talcondition'])
        self.assertFalse(self.installer.isProductInstalled('collective.behavior.talcondition'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveBehaviorTalconditionLayer is registered."""
        from collective.behavior.talcondition.interfaces import ICollectiveBehaviorTalconditionLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveBehaviorTalconditionLayer, utils.registered_layers())
