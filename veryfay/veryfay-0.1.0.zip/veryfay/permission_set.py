from veryfay.role_set import AllowRoleSet, DenyRoleSet


class PermissionSet(object):
    """Holds a list of allow or deny rules (aka roles)."""

    def __init__(self, authorization_engine):
        self._role_sets = []
        self._authorization_engine = authorization_engine

    def allow(self, role, *more_roles):
        """Register any allow rules.
        
        Args:
            role: an allow rule to add to the list of rules.
                  Either class instances or class objects with a no param constructor are allowed.
            more_roles: optional allow rules to add to list of rules.
                        Either class instances or class objects with a no param constructor are allowed.

        Returns:
            Self.
        """
        roles = [role]
        for r in more_roles: 
            roles.append(r)
        self._role_sets.append(AllowRoleSet(roles))
        return self

    def deny(self, role, *more_roles):
        """Register any deny rules.
        
        Args:
            role: a deny rule to add to the list of rules. 
                  Either class instances or class objects with a no param constructor are allowed.
            more_roles: optional deny rules to add to the list of rules.
                        Either class instances or class objects with a no param constructor are allowed.

        Returns:
            Self.
        """
        roles = [role]
        for r in more_roles: 
            roles.append(r)
        self._role_sets.append(DenyRoleSet(roles))
        return self

    @property
    def And(self):
        """Returns the container of any registered authorization activities."""
        return self._authorization_engine

    @property
    def role_sets(self):
        return self._role_sets

    @role_sets.setter
    def role_sets(self, value):
        self._role_sets = value
