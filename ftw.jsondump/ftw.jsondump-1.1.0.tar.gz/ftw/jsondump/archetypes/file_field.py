from base64 import b64encode
from ftw.jsondump.interfaces import IFieldExtractor
from plone.app.blob.interfaces import IBlobField
from plone.app.blob.interfaces import IBlobImageField
from Products.Archetypes.interfaces.field import IFileField
from Products.Archetypes.interfaces.field import IImageField
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class FileFieldExtractor(object):
    implements(IFieldExtractor)
    adapts(Interface, Interface, IFileField)

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def extract(self, name, data, config):
        value = self.field.get(self.context)

        if not value:
            return

        mimetype = self.field.getContentType(self.context)

        if config.get('filedata', True):
            data.update({'{0}:file'.format(name): b64encode(value.data)})

        data.update({'{0}:mimetype'.format(name): mimetype,
                     '{0}:size'.format(name): len(value.data),
                     '{0}:filename'.format(name): value.filename})

        file_callback = config.get('file_callback', None)
        if file_callback:
            file_callback(self.context, name, name,
                          value.data, value.filename, mimetype,
                          data)


class ImageFieldExtractor(FileFieldExtractor):
    adapts(Interface, Interface, IImageField)


class FileBlobFieldExtractor(FileFieldExtractor):
    adapts(Interface, Interface, IBlobField)


class ImageBlobFieldExtractor(FileFieldExtractor):
    adapts(Interface, Interface, IBlobImageField)
