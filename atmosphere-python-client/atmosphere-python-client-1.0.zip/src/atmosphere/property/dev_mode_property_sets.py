import atmosphere.tools


__author__ = 'paoolo'

PREFIX = '/dev_mode_property_sets'


def get_all_dev_mode_property_set(app_id=None):
    url = ''
    if app_id is not None:
        url += 'appliance_id=%s' % str(app_id)
    if len(url) > 0:
        url = '?' + url
    return atmosphere.tools.create_req(url=url)


def get_dev_mode_property_set(_id):
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(url=url)


def update_dev_mode_property_set(_id, name=None, description=None,
                                 shared=None, scalable=None,
                                 preference_cpu=1, preference_memory=1024, preference_disk=10240,
                                 security_proxy_id=1):
    _data = atmosphere.tools.get_data(locals())
    _data['id'] = _id
    body = {'dev_mode_property_set': _data}
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_PUT, url=url, body=body)
