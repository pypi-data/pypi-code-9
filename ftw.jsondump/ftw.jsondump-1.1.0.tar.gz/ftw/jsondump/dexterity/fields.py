from ftw.jsondump.interfaces import IFieldExtractor
from ftw.jsondump.interfaces import IPartial
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.utils import iterSchemata
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface
from zope.schema import getFieldsInOrder


class DexterityFieldsPartial(object):
    implements(IPartial)
    adapts(IDexterityContent, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, config):
        data = {}
        for schemata in iterSchemata(self.context):
            for name, field in getFieldsInOrder(schemata):
                extractor = getMultiAdapter(
                    (self.context, self.request, field),
                    IFieldExtractor)
                extractor.extract(name, data, config)
        return data
