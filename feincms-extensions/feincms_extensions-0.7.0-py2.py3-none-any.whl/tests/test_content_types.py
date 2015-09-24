import datetime

from django.test import TestCase

from . import factories
from .models import Dummy
from .. import content_types


class TestJsonRichTextContent(TestCase):
    model = Dummy.content_type_for(content_types.JsonRichTextContent)

    def test_json(self):
        """A JsonRichTextContent can be rendered to json."""
        text = 'Rich Text'
        pk = 42
        content = self.model(region='body', text=text, pk=pk)
        self.assertEqual(content.json(), {
            'content_type': 'rich-text',
            'html': text,
            'id': pk,
        })


class TestJsonSectionContent(TestCase):
    model = Dummy.content_type_for(content_types.JsonSectionContent)

    def test_json(self):
        """A JsonSectionContent can be rendered to json."""
        title = 'Section 1'
        richtext = 'Rich Text'
        image_type = 'image'
        copyright = 'Incuna'
        pk = 42
        created = datetime.datetime(year=2015, month=3, day=1)
        section_type = 'type1'

        image = factories.MediaFileFactory.build(
            type=image_type,
            copyright=copyright,
            created=created,
        )
        content = self.model(
            region='body',
            title=title,
            richtext=richtext,
            type=section_type,
            mediafile=image,
            pk=pk,
        )

        expected = {
            'content_type': 'section',
            'id': pk,
            'title': title,
            'html': richtext,
            'type': section_type,
            'mediafile': {
                'url': image.file.url,
                'type': image_type,
                'created': created,
                'copyright': copyright,
                'file_size': image.file.size,
            },
        }
        self.assertEqual(content.json(), expected)

    def test_json_no_mediafile(self):
        """A JsonSectionContent can be rendered to json."""
        title = 'Section 1'
        richtext = 'Rich Text'
        pk = 42
        section_type = 'type1'

        content = self.model(
            pk=pk,
            region='body',
            title=title,
            type=section_type,
            richtext=richtext,
            mediafile=None,
        )

        expected = {
            'content_type': 'section',
            'id': pk,
            'title': title,
            'html': richtext,
            'mediafile': None,
            'type': section_type,
        }
        self.assertEqual(content.json(), expected)


class TestJsonMediaFileContent(TestCase):
    model = Dummy.content_type_for(content_types.JsonMediaFileContent)

    def test_json(self):
        """A JsonMediaFileContent can be rendered to json."""
        image_type = 'image'
        copyright = 'Incuna'
        created = datetime.datetime(year=2015, month=3, day=1)
        pk = 42

        image = factories.MediaFileFactory.create(
            type=image_type,
            copyright=copyright,
            created=created,
        )
        caption = 'Image file'
        image.translations.create(caption=caption)
        content = self.model(region='body', mediafile=image, pk=pk)

        expected = {
            'content_type': 'media-file',
            'id': pk,
            'url': image.file.url,
            'type': image_type,
            'created': created,
            'copyright': copyright,
            'file_size': image.file.size,
            'caption': caption,
        }
        self.assertEqual(content.json(), expected)

    def test_json_caption_fallback(self):
        """The caption falls back to the file name."""
        image = factories.MediaFileFactory.create()
        content = self.model(mediafile=image)
        caption = content.json()['caption']
        self.assertEqual(caption, image.file.name)
