from grokcore import component
from zope.interface import implementer
from zope.security.interfaces import IPrincipal

from bst.pygasus.wsgi.interfaces import IRequest
from bst.pygasus.security.interfaces import IAuthenticatedPrincipalFactory


@implementer(IPrincipal)
class Principal(object):

    def __init__(self, id, title=None, description=None):
        self.id = id
        self.title = title
        self.description = description


@implementer(IAuthenticatedPrincipalFactory)
class SimpleAuthenticatedPrincipalFactory(component.MultiAdapter):
    """ Default principal factory thats do nothing
        else as return the same principal. If you need to
        transform your principal so override this adapter.
    """

    component.adapts(IPrincipal, IRequest)

    def __init__(self, principal, request):
        self.principal = principal
        self.request = request

    def __call__(self, auth):
        return self.principal
