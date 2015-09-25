"""
Contains signal unit tests.
"""
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from taggit.models import Tag
from wagtail.wagtailcore.models import Page
from wagtail.tests.testapp.models import TaggedPage
from ..models import (
    Entry,
    EntryTag
)


class TestSignals(TestCase):
    def setUp(self):
        # Get the root page.
        self.root_page = Page.objects.get(id=2)

        # Create a tag.
        self.tag = Tag.objects.create(name='Test')

        # Add a page.
        self.child_page = self.root_page.add_child(instance=TaggedPage(
            title   = 'Test Page',
            slug    = 'test-page'
        ))

        # Add a tag to the page.
        self.child_page.tags.through.objects.create(
            content_object  = self.child_page,
            tag             = self.tag
        )

    def test_create_entry_tag(self):
        self.assertTrue(
            EntryTag.objects.filter(
                entry__content_type = ContentType.objects.get_for_model(self.child_page),
                entry__object_id    = self.child_page.id,
                tag                 = self.tag
            ).exists()
        )

    def test_delete_entry_tag(self):
        self.child_page.tags.through.objects.filter(
            tag=self.tag
        ).delete()

        self.assertEqual(EntryTag.objects.count(), 0)

    def test_delete_entry(self):
        self.child_page.delete()

        self.assertEqual(Entry.objects.count(), 0)

    def test_update_entry_attributes(self):
        self.child_page.title = 'Updated Test Page'
        self.child_page.save()

        entry = Entry.objects.get(
            content_type    = ContentType.objects.get_for_model(self.child_page),
            object_id       = self.child_page.id
        )

        self.assertEqual(entry.title, self.child_page.title)
