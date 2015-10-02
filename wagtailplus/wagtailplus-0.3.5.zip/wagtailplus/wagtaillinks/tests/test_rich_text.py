"""
Contains rich-text unit tests.
"""
from django.test import TestCase
from django.utils.html import escape

from ..models import Link
from ..rich_text import LinkHandler


class TestLinkHandler(TestCase):
    def setUp(self):
        self.model = Link.objects.create(
            link_type       = Link.LINK_TYPE_EXTERNAL,
            title           = 'Test Link',
            external_url    = 'http://test.com'
        )

    def test_get_db_attribute(self):
        tag = {'data-id': self.model.pk}

        self.assertEqual(
            LinkHandler.get_db_attributes(tag),
            {'id': self.model.pk}
        )

    def test_expand_db_attributes(self):
        self.assertEqual(
            LinkHandler.expand_db_attributes(
                {'id': self.model.pk},
                True
            ),
            '<a data-linktype="link" data-id="{0}" href="{1}" title="{2}">'.format(
                self.model.pk,
                escape(self.model.get_absolute_url()),
                self.model.title
            )
        )

    def test_expand_db_attributes_bad_link(self):
        self.assertEqual(
            LinkHandler.expand_db_attributes(
                {'id': 42},
                True
            ),
            '<a>'
        )
