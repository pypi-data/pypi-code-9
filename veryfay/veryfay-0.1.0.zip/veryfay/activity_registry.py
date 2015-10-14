from veryfay.activity import Container


class ActivityRegistry(object):

    def __init__(self):
        self._registered_permissions = {}

    def add(self, activity, permission_set):
        if isinstance(activity, Container):
            for a in activity.activities:
                self.add(a, permission_set)
        else:
            self.add_activity_permissions(activity, permission_set)

    def add_activity_permissions(self, activity, permission_set):
        activity_permission_list = []
        key = (type(activity), activity.target)
        if key in self._registered_permissions:
            activity_permission_list = self._registered_permissions[key]
        activity_permission_list.append(permission_set)
        self._registered_permissions[key] = activity_permission_list

    def get(self, activity):
        key = (type(activity), activity.target)
        if key in self._registered_permissions:
            return self._registered_permissions[key]
        else:
            msg = 'no registered activity of type {0}'.format(key)
            raise KeyError(msg)
