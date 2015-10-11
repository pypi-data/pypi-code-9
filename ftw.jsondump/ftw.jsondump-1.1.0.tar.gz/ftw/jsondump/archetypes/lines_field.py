from ftw.jsondump.interfaces import IFieldExtractor
from Products.Archetypes.interfaces.field import ILinesField
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class LinesFieldExtractor(object):
    implements(IFieldExtractor)
    adapts(Interface, Interface, ILinesField)

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def extract(self, name, data, config):
        value = list(self.field.get(self.context))
        data.update({name: value})
