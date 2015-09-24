from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.section.models import SectionContent


class JsonRichTextContent(RichTextContent):
    class Meta(RichTextContent.Meta):
        abstract = True

    def json(self, **kwargs):
        """Return a json serializable dictionary containing the content."""
        return {
            'content_type': 'rich-text',
            'html': self.text,
            'id': self.pk,
        }


def mediafile_data(mediafile):
    """Return json serializable data for the mediafile."""
    if mediafile is None:
        return None
    return {
        'url': mediafile.file.url,
        'type': mediafile.type,
        'created': mediafile.created,
        'copyright': mediafile.copyright,
        'file_size': mediafile.file_size,
    }


class JsonSectionContent(SectionContent):
    class Meta(SectionContent.Meta):
        abstract = True

    def json(self, **kwargs):
        """Return a json serializable dictionary containing the content."""
        return {
            'id': self.pk,
            'content_type': 'section',
            'title': self.title,
            'type': self.type,
            'html': self.richtext,
            'mediafile': mediafile_data(self.mediafile),
        }


class JsonMediaFileContent(MediaFileContent):
    class Meta(MediaFileContent.Meta):
        abstract = True

    def json(self, **kwargs):
        """Return a json serializable dictionary containing the content."""
        data = mediafile_data(self.mediafile)
        data['content_type'] = 'media-file'
        data['id'] = self.pk
        try:
            caption = self.mediafile.translation.caption
        except AttributeError:
            caption = self.mediafile.file.name
        data['caption'] = caption
        return data
