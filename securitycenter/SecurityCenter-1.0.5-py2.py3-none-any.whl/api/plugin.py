from base64 import b64decode
from ._base import Module, extract_value
from ..util import PagedResult


class Plugin(Module):
    _name = 'plugin'

    def _fetch(self, action, since=None, type=None, sort=None, desc=True, page=1, page_size=100, **filter):
        filter_field, filter_string = filter.popitem() if filter else (None, None)
        input = self._sc._process_input({
            'since': since,
            'type': type,
            'sortField': sort,
            'sortDirection': None if desc else 'asc',
            'size': page_size,
            'offset': page_size * (page - 1),
            'filterField': filter_field,
            'filterString': filter_string,
        })
        return self._request(action, input, page_class=PluginPagedResult)

    def init(self, since=None, type=None, sort=None, desc=True, page=1, page_size=100, **filter):
        return self._fetch('init', since=since, type=type, sort=sort, desc=desc, page=page, page_size=page_size, **filter)

    @extract_value('plugins')
    def get_page(self, since=None, type=None, sort=None, desc=True, page=1, page_size=100, **filter):
        return self._fetch('getPage', since=since, type=type, sort=sort, desc=desc, page=page, page_size=page_size, **filter)

    @extract_value('plugin')
    def get_details(self, id):
        return self._request('getDetails', {
            'pluginID': id
        })

    def get_source(self, id, type=None):
        """Returns the NASL source of a plugin.
        The API returns the script base64 encoded.  This is decoded and returned in plain text.
        If the script is encrypted, the result will say something about that instead of the source.

        :param id: plugin id
        :return:
        """

        return b64decode(self._request('getSource', {
            'pluginID': id,
            'type': type
        })['source']).decode('utf8')

    @extract_value('families')
    def get_families(self):
        return self._request('getFamilies')

    @extract_value('families')
    def get_matching_families(self, since=None, type=None, **filter):
        return self._fetch('getMatchingFamilies', since=since, type=type, **filter)

    @extract_value('families')
    def get_plugins(self, family_ids=None, type=None, since=None):
        return self._request('getPlugins', {
            'families': [{'id': id} for id in family_ids] if family_ids else None,
            'type': type,
            'since': since
        })

    def update(self, type):
        return self._request('update', {
            'type': type
        })

    def clear(self, type):
        return self._request('clear', {
            'type': type
        })

    def upload(self, type, file):
        return self._request('upload', {
            'type': type,
            'filename': self._sc.file.name_or_upload(file)
        })


class PluginPagedResult(PagedResult):
    _key = 'plugins'

    @staticmethod
    def _can_page(data):
        return 'pluginCount' in data

    def _set_page(self, input, data):
        size = int(input['size']) if 'size' in input else 100
        start = int(input['offset']) if 'offset' in input else 0
        self.page_size = size
        self.page = start // size + 1 if size > 0 else 1

    def _set_total(self, input, data):
        self.total = int(data['pluginCount'])

    def _next_input(self):
        input = self.input.copy()
        input['size'] = self.page_size
        input['offset'] = self.page_size * self.page
        return input
