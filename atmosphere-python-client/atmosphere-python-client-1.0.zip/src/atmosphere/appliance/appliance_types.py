import atmosphere.tools

__author__ = 'paoolo'

PREFIX = '/appliance_types'


def get_all_appliance_types(name=None):
    """
    Get a list of appliance types.

    :param name: any string (optional)
    :return:
    """
    url = ''
    if name is not None:
        url += 'name=%s' % str(name)
    if len(url) > 0:
        url = '&' + url
    return atmosphere.tools.create_req(url=url)


get_all_app_type = get_all_appliance_types


def get_app_type(_id):
    """
    Get detailed data about appliance set.

    :param _id: integer (required)
    :return:
    """
    url = '/%d' % int(_id)
    return atmosphere.tools.create_req(url=url)


def create_app_type(appliance_id,
                    name=None, description=None,
                    shared=None, scalable=None, visible_to=None,
                    preference_cpu=None, preference_memory=None, preference_disk=None,
                    author_id=None, security_proxy_id=None):
    """
    Create new appliance type.

    :param appliance_id: integer (required)
    :param name: any string (optional)
    :param description: any string (optional)
    :param shared: boolean (optional)
    :param scalable: boolean (optional)
    :param visible_to: enum of: owner, developer, all (optional)
    :param preference_cpu: integer (optional)
    :param preference_memory: integer (optional)
    :param preference_disk: integer (optional)
    :param author_id: integer (optional)
    :param security_proxy_id: integer (optional)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    body = {'appliance_type': _data}
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_POST, body=body)


def update_app_type(_id, appliance_id=None, name=None, description=None,
                    shared=None, scalable=None, visible_to=None,
                    preference_cpu=None, preference_memory=None, preference_disk=None,
                    author_id=None, security_proxy_id=None):
    """
    Create new appliance type.

    :param _id: integer (required)
    :param appliance_id: integer (optional)
    :param name: any string (optional)
    :param description: any string (optional)
    :param shared: boolean (optional)
    :param scalable: boolean (optional)
    :param visible_to: enum of: owner, developer, all (optional)
    :param preference_cpu: integer (optional)
    :param preference_memory: integer (optional)
    :param preference_disk: integer (optional)
    :param author_id: integer (optional)
    :param security_proxy_id: integer (optional)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    _data['id'] = _id
    body = {'appliance_type': _data}
    url = '/%s' % str(_id)
    _data = atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_PUT, url=url, body=body)


def delete_app_type(_id):
    """
    Delete appliance type.

    :param _id: positive decimal number (required)
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(method=atmosphere.tools.HTTP_DELETE, url=url)