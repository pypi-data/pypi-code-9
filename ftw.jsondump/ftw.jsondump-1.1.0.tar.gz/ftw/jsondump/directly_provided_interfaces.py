from ftw.jsondump.interfaces import IPartial
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope.interface import directlyProvidedBy


class InterfacesPartial(object):
    implements(IPartial)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, config):
        return {'_directly_provided': map(lambda item: item.__identifier__,
                                          directlyProvidedBy(self.context))}
