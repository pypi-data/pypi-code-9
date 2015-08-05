from django.core.urlresolvers import reverse
from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from wagtailsettings.registry import Registry

from tests.app.models import NotYetRegisteredSetting


class TestRegister(TestCase, WagtailTestUtils):
    def setUp(self):
        self.registry = Registry()
        self.login()

    def test_register(self):
        self.assertNotIn(NotYetRegisteredSetting, self.registry.models)
        NowRegisteredSetting = self.registry.register(NotYetRegisteredSetting)
        self.assertIn(NotYetRegisteredSetting, self.registry.models)
        self.assertIs(NowRegisteredSetting, NotYetRegisteredSetting)

    def test_icon(self):
        admin = self.client.get(reverse('wagtailadmin_home'))
        self.assertContains(admin, 'icon icon-tag')
