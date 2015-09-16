from six import iteritems
from ._base import Module, extract_value


class User(Module):
    _name = 'user'

    @extract_value('users')
    def init(self):
        return self._request('init')

    @extract_value('results')
    def query(self, tool='listusers', sort='username', desc=False, page=1, page_size=100, **filters):
        return self._request('query', {
            'filters': [{'filterName': key, 'value': value} for key, value in iteritems(filters)],
            'tool': tool,
            'sortField': sort,
            'sortDir': 'desc' if desc else None,
            'startOffset': page_size * (page - 1),
            'endOffset': page_size * page - 1
        })

    def change_password(self, password):
        return self._request('changePassword', {
            'password': password
        })

    def get_coverage(self, user_id, group_id):
        return self._request('getCoverage', {
            'userID': user_id,
            'currentGroupID': group_id
        })


class Admin(Module):
    _name = 'admin'

    @extract_value('users')
    def init(self):
        return self._request('init')


class UserPrefs(Module):
    _name = 'userPrefs'

    @extract_value('preferences')
    def init(self):
        return self._request('init')

    def set(self, user_id=None, **prefs):
        prefs['userID'] = user_id
        return self._request('set', prefs)

    def set_module_prefs(self, module=None, tool=None, columns=None, filters=None, chart=None):
        return self._request('setModulePrefs', {
            'module': module,
            'tool': tool,
            'columns': columns,
            'filters': filters,
            'chart': chart
        })
