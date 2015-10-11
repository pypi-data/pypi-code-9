from ftw.jsondump.interfaces import IFieldExtractor
from Products.Archetypes.interfaces.field import ITextField
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class TextFieldExtractor(object):
    implements(IFieldExtractor)
    adapts(Interface, Interface, ITextField)

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def extract(self, name, data, config):
        value = self.field.getRaw(self.context)
        mimetype = self.field.getContentType(self.context)
        data.update({name: value,
                     '{0}:mimetype'.format(name): mimetype})
