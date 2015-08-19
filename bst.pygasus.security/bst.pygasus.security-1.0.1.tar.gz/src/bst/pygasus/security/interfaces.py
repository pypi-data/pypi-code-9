from zope.interface import Interface
from zope.authentication import interfaces as authentication


class IAuthentication(authentication.IAuthentication,
                      authentication.ILogout,
                      authentication.ILogoutSupported):
    pass


class ICredentialsPlugin(Interface):
    """Handles credentials extraction and challenges per request.
    """

    def extractCredentials(request):
        """Ties to extract credentials from a request.

        A return value of None indicates that no credentials could be found.
        Any other return value is treated as valid credentials.
        """

    def challenge(request):
        """Possibly issues a challenge.

        This is typically done in a protocol-specific way.

        If a challenge was issued, return True, otherwise return False.
        """

    def logout(request):
        """Possibly logout.

        If a logout was performed, return True, otherwise return False.
        """


class IAuthenticatorPlugin(Interface):
    """ Authenticates a principal using credentials.
    An authenticator may also be responsible for providing information
    about and creating principals.
    """

    def authenticateCredentials(credentials):
        """Authenticates credentials.

        If the credentials can be authenticated, return an object that provides
        IPrincipalInfo. If the plugin cannot authenticate the credentials,
        returns None.
        """

    def principalInfo(id):
        """Returns an IPrincipalInfo object for the specified principal id.

        If the plugin cannot find information for the id, returns None.
        """


class IAuthenticatedPrincipalFactory(Interface):

    def __init__(self, principal, request):
        """ MultiAdapter for IPrincipal and IRequest
        """

    def __call__(self, auth):
        """ auth is a instance thats provide IAuthentication
        """
