from ftw.jsondump.interfaces import IPartial
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class LocalRolesPartial(object):
    implements(IPartial)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, config):
        rolesmapping = {}
        data = {'__ac_local_roles__': rolesmapping,
                '__ac_local_roles_block__': False}

        if getattr(self.context, '__ac_local_roles__', False):
            for principal, roles in self.context.__ac_local_roles__.items():
                rolesmapping.update({principal: list(roles)})

        data['__ac_local_roles_block__'] = getattr(
            self.context,
            '__ac_local_roles_block__',
            False)
        return data
