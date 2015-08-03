from grokcore import component
from zope.interface import implementer

from bst.pygasus.session.interfaces import ISession
from bst.pygasus.security.principal import Principal
from bst.pygasus.security.interfaces import ICredentialsPlugin
from bst.pygasus.security.interfaces import IAuthenticatorPlugin


REMOTEUSER = 'remoteuser'
FORM_LOGIN = 'loginform.login'
FORM_PASSWORD = 'loginform.password'
SESSION_CREDENTIALS = 'bst.pygasus.security.session.credentials'


@implementer(ICredentialsPlugin)
class RemoteCredentialsPlugin(component.GlobalUtility):
    """ Fetch remote user from environment variable. This variable must
        be set via rewrite proxy e.g. apache. Normally this plugin
        works with RemoteAuthenticatorPlugin.
    """
    component.name('remoteuser')

    def extractCredentials(self, request):
        """ fetch remote user in the nvironment variable
            and create credentials with it.
        """
        remote_user = request.environ.get('REMOTE_USER', None)
        if remote_user is None:
            return None
        return {REMOTEUSER: remote_user}

    def challenge(self, request):
        return False

    def logout(self, request):
        return False


@implementer(ICredentialsPlugin)
class RequestCredentialsPlugin(component.GlobalUtility):
    """ Fetch credentials from HTTP headers.
    """
    component.name('request_credentials')

    def extractCredentials(self, request):
        """ fetch remote user in the http headers
            and create credentials with it.
        """
        session = ISession(request)
        cred = dict(login=request.params.get(FORM_LOGIN, None),
                    password=request.params.get(FORM_PASSWORD, None))
        if None in cred.values():
            if SESSION_CREDENTIALS in session:
                return session[SESSION_CREDENTIALS]
            else:
                return None
        session[SESSION_CREDENTIALS] = cred
        return cred

    def challenge(self, request):
        return False

    def logout(self, request):
        session = ISession(request)
        re = SESSION_CREDENTIALS in session
        del session[SESSION_CREDENTIALS]
        return re


@implementer(IAuthenticatorPlugin)
class RemoteAuthenticatorPlugin(component.GlobalUtility):

    component.name('remoteuser')

    def authenticateCredentials(self, credentials):
        if REMOTEUSER not in credentials:
            return None
        return self.principalInfo(credentials[REMOTEUSER])

    def principalInfo(self, id):
        return Principal(id)
