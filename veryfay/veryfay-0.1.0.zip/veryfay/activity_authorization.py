from veryfay.authorization_exception import AuthorizationException
from veryfay.permission_verifier import PermissionVerifier


class ActivityAuthorization(object):
    """Verifier for an authorization activity."""

    def __init__(self, activity, activity_registry):
        self._activity = activity
        self._activity_registry = activity_registry

    def is_allowing(self, principal, *extra_info):
        """Check authorization for principal and optional extra info.
        
        Args:
            principal: principal information to be checked for authorization.
            extra_info: optional extra info to be checked for authorization.
        
        Returns:
            When authorization result is true, 
            an object containing the result of the verification as a boolean
            and details about the verified rules as a string.
            Otherwise raises a AuthorizationException
            containing details about the verified rules.
        """
        return self._authorize(principal, *extra_info)

    def verify(self, principal, *extra_info):
        """Check authorization for principal and optional extra info.
        
        Args:
            principal: principal information to be checked for authorization.
            extra_info: optional extra info to be checked for authorization.
        
        Returns:
            An object containing the result of the verification as a boolean
            and details about the verified rules as a string.
        """
        result = self._authorize(principal, *extra_info)
        if result.is_success:
            return result.details
        else:
            raise AuthorizationException(result.details)

    def _authorize(self, principal, *extra_info):
        try:
            activity_permissions = self._activity_registry.get(self._activity)
        except KeyError as e:
            return IsAllowingResult(False, str(e))

        try:
            details = PermissionVerifier.verify(activity_permissions, principal, *extra_info)
        except AuthorizationException as e:
            return IsAllowingResult(False, str(e))

        return IsAllowingResult(True, details)


class IsAllowingResult(object):

    def __init__(self, is_allowing, details):
        self._is_allowing = is_allowing
        self._details = details

    @property
    def is_success(self):
        return self._is_allowing

    @property
    def is_failure(self):
        return not self._is_allowing

    @property
    def details(self):
        return self._details
