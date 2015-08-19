from grokcore import component

from zope.interface import implementer
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.component import getMultiAdapter

from zope.authentication.interfaces import PrincipalLookupError

from bst.pygasus.security import interfaces
from bst.pygasus.security.interaction import ANONYMOUSE
from bst.pygasus.core.interfaces import IApplicationContext

from zope.authentication.interfaces import IAuthentication


@implementer(interfaces.IAuthentication)
class PluggableUtility(component.GlobalUtility):
    """ Default plugable authentication utility
        with similar functionality as zope framework.
    """

    def _credentials_pluggins(self):
        application = getSite()
        if application is None:
            return None
        for name in application.credentials_pluggins:
            pluggin = queryUtility(interfaces.ICredentialsPlugin, name=name)
            if pluggin is not None:
                yield pluggin

    def _authentication_pluggins(self):
        application = getSite()
        if application is None:
            return None
        for name in application.authentication_pluggins:
            pluggin = queryUtility(interfaces.IAuthenticatorPlugin, name=name)
            if pluggin is not None:
                yield pluggin

    def authenticate(self, request):
        for cred in self._credentials_pluggins():
            for auth in self._authentication_pluggins():
                credential_dict = cred.extractCredentials(request)
                if credential_dict is None:
                    continue
                principal = auth.authenticateCredentials(credential_dict)
                if principal is not None:
                    return getMultiAdapter((principal, request),
                                           interfaces.IAuthenticatedPrincipalFactory)(self)
        return None

    def unauthenticatedPrincipal(self):
        return ANONYMOUSE

    def unauthorized(self, id, request):
        raise NotimplementedError('just not implemented at the moment')

    def getPrincipal(self, id):
        for auth in self._authentication_pluggins():
            principal = auth.principalInfo(id)
            if principal is None:
                continue
            return principal
        if self.unauthenticatedPrincipal() is not None:
            return self.unauthenticatedPrincipal()
        raise PrincipalLookupError(id)

    def logout(self, request):
        for cred in self._credentials_pluggins():
            if cred.logout(request):
                return True
        return False
