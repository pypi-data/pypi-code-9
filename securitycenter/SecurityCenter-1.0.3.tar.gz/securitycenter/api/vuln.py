from six import iteritems, string_types
from ._base import Module, extract_value


class Vuln(Module):
    _name = 'vuln'

    def init(self):
        return self._request('init')

    @extract_value('results')
    def query(self, tool='listvuln', source='cumulative', view=None, scan=None, sort=None, sort_dir=None, page=1, page_size=100, short_form=None, **filters):
        if scan is not None:
            source = 'individual'

            if view is None:
                view = 'all'

        filter_items = []

        for key, value in iteritems(filters):
            op, value = ('=', value) if isinstance(value, string_types) else value
            filter_items.append({'filterName': key, 'operator': op, 'value': value})

        return self._request('query', {
            'filters': filter_items,
            'tool': tool,
            'sourceType': source,
            'view': view,
            'scanID': scan,
            'sortField': sort,
            'sortDir': sort_dir,
            'startOffset': page_size * (page - 1),
            'endOffset': page_size * page - 1,
            'shortForm': short_form
        })

    @extract_value('records')
    def get_ip(self, ip, repo_ids=None, dns=None, mac=None, netbios=None, score=None, info=None, low=None, medium=None, high=None, critical=None, os=None):
        return self._request('getIP', {
            'ip': ip,
            'repositories': [{'id': r_id} for r_id in repo_ids] if repo_ids else None,
            'dnsName': dns,
            'macAddress': mac,
            'netbiosName': netbios,
            'score': score,
            'severityInfo': info,
            'severityLow': low,
            'severityMedium': medium,
            'severityHigh': high,
            'severityCritical': critical,
            'os': os
        })

    def get_asset(self, id):
        return self._request('getAsset', {
            'id': id
        })

    def get_asset_intersections(self, ip, asset_ids, dns=None, repo_ids=None):
        return self._request('getAssetIntersections', {
            'ip': ip,
            'assetIDs': [{'id': a_id} for a_id in asset_ids],
            'dnsName': dns,
            'repositories': [{'id': r_id} for r_id in repo_ids] if repo_ids else None
        })

    def download(self, columns, tool='listvuln', source='cumulative', view=None, scan=None, sort=None, sort_dir=None, page=1, page_size=100, short_form=None, **filters):
        filter_items = []

        for key, value in iteritems(filters):
            op, value = ('=', value) if isinstance(value, string_types) else value
            filter_items.append({'filterName': key, 'operator': op, 'value': value})

        return self._request('download', {
            'columns': columns,
            'filters': filter_items,
            'tool': tool,
            'sourceType': source,
            'view': view,
            'scanID': scan,
            'sortField': sort,
            'sortDir': sort_dir,
            'startOffset': page_size * (page - 1),
            'endOffset': page_size * page - 1,
            'shortForm': short_form
        }, parse=False).content
