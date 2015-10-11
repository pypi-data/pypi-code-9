from Acquisition import aq_inner
from Acquisition import aq_parent
from ftw.jsondump.interfaces import IPartial
from OFS.interfaces import IOrderedContainer
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class MetadataPartial(object):
    implements(IPartial)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, config):
        parent = aq_parent(aq_inner(self.context))
        klass = self.context.__class__

        data = {'_classname': klass.__name__,
                '_class': klass.__module__ + '.' + klass.__name__,
                '_id': self.context.getId(),
                '_owner': self.context.getOwner().getId(),
                '_path': '/'.join(self.context.getPhysicalPath()),
                '_type': self.context.portal_type}

        ordered_parent = IOrderedContainer(parent, None)
        if ordered_parent:
            data['_obj_position_in_parent'] = ordered_parent.getObjectPosition(
                self.context.getId())

        return data
