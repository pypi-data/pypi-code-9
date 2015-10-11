from ftw.jsondump.interfaces import IFieldExtractor
from Products.Archetypes.interfaces.field import IField
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class BaseFieldExtrator(object):
    implements(IFieldExtractor)
    adapts(Interface, Interface, IField)

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def extract(self, name, data, config):
        value = self.convert(self.field.get(self.context))
        data.update({name: value})

    def convert(self, value):
        return value
