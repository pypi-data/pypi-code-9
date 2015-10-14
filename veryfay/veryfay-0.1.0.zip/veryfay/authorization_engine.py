from veryfay.activity_authorization import ActivityAuthorization
from veryfay.activity_registry import ActivityRegistry
from veryfay.permission_set import PermissionSet


class AuthorizationEngine(object):
    """Holds any registered authorization activities."""

    def __init__(self):
        self._activity_registry = ActivityRegistry()

    def register(self, activity, *more_activities):
        """Register any authorization activities.
        
        Args:
            activity: required authorization activity to register.
            more_activities: optional authorization activities to register.

        Returns:
            A container for the authorization rules
            associated to the registered authorization activities.
        """
        ps = PermissionSet(self)
        self._activity_registry.add(activity, ps)
        for a in more_activities:
            self._activity_registry.add(a, ps)
        return ps

    def __call__(self, activity):
        """Creates a verifier for an authorization activity.
        
        Args:
            activity: authorization activity to verify.

        Returns:
            A verifier to check the input activity.
        """
        return ActivityAuthorization(activity, self._activity_registry)

