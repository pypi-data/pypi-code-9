from ftw.jsondump.interfaces import IFieldExtractor
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope.schema.interfaces import IField


class PlainFieldExtractor(object):
    implements(IFieldExtractor)
    adapts(Interface, Interface, IField)

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def extract(self, name, data, config):
        storage = self.field.interface(self.context)
        value = getattr(storage, name)
        value = self.convert(value)
        data.update({self.key: value})

    @property
    def key(self):
        return '.'.join((
                self.field.interface.__identifier__,
                self.field.__name__))

    def convert(self, value):
        return value
