from ftw.jsondump.interfaces import IPartial
from plone.uuid.interfaces import IUUID
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class UIDPartial(object):
    implements(IPartial)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, config):
        return {'_uid': IUUID(self.context)}
