import inspect


class RoleSet(object):

    DEFINE_CONTAINS = 'error: {}\n role {} should define a "contains(self, principal, *extra_info)" method that returns a boolean value'

    def __init__(self, roles):
        self._roles = roles

    def check(self, principal, *extra_info):
        result = True
        def visitor(role):
            if inspect.isclass(role):
                role = role()
            nonlocal result
            try:
                contains = self._contains(role, principal, *extra_info)
                if not contains:
                    result = False
            except (AttributeError, TypeError) as e:
                raise NotImplementedError(RoleSet.DEFINE_CONTAINS.format(e, role))
        self._traverse(self._roles, visitor)
        return result

    def get_msg(self, principal, *extra_info):
        msg = []
        break_it = False
        def visitor(role):
            if inspect.isclass(role):
                role = role()
            nonlocal break_it
            try:
                if not break_it:
                    contains = self._contains(role, principal, *extra_info)
                    if contains:
                        msg.append('{0} contains {1} and {2} AND'
                                   .format(role, principal, extra_info))
                    else:
                        msg.append('{0} DOES NOT contain {1} and {2}'
                                   .format(role, principal, extra_info))
                        break_it = True
            except (AttributeError, TypeError) as e:
                raise NotImplementedError(RoleSet.DEFINE_CONTAINS.format(e, role))
        self._traverse(self._roles, visitor)
        return '\n'.join(msg)

    def _contains(self, role, principal, *extra_info):
        contains = role.contains(principal, *extra_info)
        if not isinstance(contains, bool):
            raise TypeError("{}.'contains' does not return a boolean value".format(role))
        return contains

    def _traverse(self, roles, visitor):
        for role in roles:
            visitor(role)

    @property
    def roles(self):
        return self._roles


class AllowRoleSet(RoleSet):
    pass


class DenyRoleSet(RoleSet):
    pass