from ftw.jsondump.interfaces import IFieldExtractor
from plone.uuid.interfaces import IUUID
from Products.Archetypes.interfaces.field import IReferenceField
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class ReferenceFieldExtractor(object):
    implements(IFieldExtractor)
    adapts(Interface, Interface, IReferenceField)

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def extract(self, name, data, config):

        references = self.field.get(self.context)

        key_path = '{0}:path'.format(name)
        key_uuid = '{0}:uuid'.format(name)
        data.update({key_path: self.get_paths(references),
                     key_uuid: self.get_uuids(references)})

    def get_paths(self, references):
        if not references:
            return ''
        elif isinstance(references, list):
            return map(lambda item: '/'.join(item.getPhysicalPath()),
                       references)
        else:
            # Single reference field
            return '/'.join(references.getPhysicalPath())

    def get_uuids(self, references):
        if not references:
            return ''
        elif isinstance(references, list):
            return map(lambda item: IUUID(item), references)
        else:
            # Single references field
            return IUUID(references)
