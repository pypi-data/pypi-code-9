"""
Contains wagtail hook unit tests.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils


class TestWagtailHooks(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

    def test_summary_item(self):
        response = self.client.get(
            reverse('wagtailadmin_home')
        )

        self.assertTemplateUsed(
            response,
            'wagtaillinks/homepage/site_summary_links.html'
        )
        self.assertTrue(
            'total_links' in response.context
        )
