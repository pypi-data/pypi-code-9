from ._base import Module, extract_value


class Asset(Module):
    _name = 'asset'

    @extract_value('assets')
    def init(self):
        return self._request('init')

    def get_details(self, id):
        return self._request('getDetails', {
            'id': id
        })

    @extract_value('viewableIPs')
    def get_ips(self, id, ips_only=False):
        return self._request('getIPs', {
            'id': id,
            'ipsOnly': ips_only
        })

    @extract_value('hostnames')
    def test_ldap_query(self, base, filter):
        return self._request('testLDAPQuery', {
            'searchBase': base,
            'searchString': filter
        })

    def get_templates(self, category=None, search=None):
        return self._request('getTemplates', {
            'categoryID': category,
            'searchString': search
        })
