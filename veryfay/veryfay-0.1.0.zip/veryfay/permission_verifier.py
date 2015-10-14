from veryfay.authorization_exception import AuthorizationException
from veryfay.role_set import AllowRoleSet, DenyRoleSet


class PermissionVerifier(object):

    @classmethod
    def verify(cls, activity_permissions, principal, *extra_info):
        res_msg = []

        for ap in activity_permissions:
            deny_role_sets = filter(lambda x: isinstance(x, DenyRoleSet), ap.role_sets)

            for deny_role_set in deny_role_sets:
                msg = deny_role_set.get_msg(principal, *extra_info)

                if deny_role_set.check(principal, *extra_info):
                    res_msg.append('### DENY SET => TRUE: {}'.format(msg))
                    raise AuthorizationException(res_msg)
                else:
                    res_msg.append('--- DENY SET => FALSE: {}'.format(msg))

        for ap in activity_permissions:
            allow_role_sets = filter(lambda x: isinstance(x, AllowRoleSet), ap.role_sets)

            for allow_role_set in allow_role_sets:
                msg = allow_role_set.get_msg(principal, *extra_info)

                if allow_role_set.check(principal, *extra_info):
                    res_msg.append('### ALLOW SET => TRUE: {}'.format(msg))
                    return res_msg
                else:
                    res_msg.append('--- ALLOW SET => FALSE: {}'.format(msg))

        raise AuthorizationException("NO MATCHING ROLE SET FOUND" if not res_msg else res_msg)
