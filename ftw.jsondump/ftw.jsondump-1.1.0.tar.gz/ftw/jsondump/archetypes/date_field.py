from ftw.jsondump.interfaces import IFieldExtractor
from Products.Archetypes.interfaces.field import IDateTimeField
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class DateFieldExtractor(object):
    implements(IFieldExtractor)
    adapts(Interface, Interface, IDateTimeField)

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def extract(self, name, data, config):
        key = '{0}:date'.format(name)
        value = str(self.field.get(self.context))
        data.update({key: value})
