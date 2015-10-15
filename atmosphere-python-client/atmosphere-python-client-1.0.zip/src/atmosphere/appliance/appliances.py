import atmosphere.tools

__author__ = 'paoolo'

PREFIX = '/appliances'


def get_all_app(_all=False):
    """
    Get list of all appliance which belong to you.

    :param _all: boolean, if you are an admin, you can request to get all existing appliances
    :return:
    """
    url = '?all=true' if _all else ''
    return atmosphere.tools.create_req(url=url)


def get_app(_id):
    """
    Get all details of an appliance.

    :param _id: positive decimal number, ID of an appliance (required)
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(url=url)


def get_app_endpoints(_id):
    """
    Get all endpoints of selected appliance.

    :param _id: positive decimal number, ID of an appliance (required)
    :return:
    """
    url = '/%s/endpoints' % str(_id)
    return atmosphere.tools.create_req(url=url)


def create_app(appliance_set_id, configuration_template_id,
               name=None, user_key_id=None, params=None):
    """
    Create new appliance.

    :param appliance_set_id: positive decimal number, ID of appliance set (required)
    :param configuration_template_id: positive decimal number, ID of configuration template connected with AT (required)
    :param name: any string (optional)
    :param user_key_id: positive decimal number (optional, only in development mode)
    :param params: a dict of params
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    body = {'appliance': _data}
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_POST, body=body)


def update_app(_id, name=None):
    """
    Update appliance name.

    :param _id: positive decimal number, ID of appliance (required)
    :param name: any string (optional)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    _data['id'] = _id
    body = {'appliance': _data}
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_PUT, url=url, body=body)


def delete_app(_id):
    """
    Delete appliance.

    :param _id: positive decimal number, ID of appliance (required)
    :return:
    """
    url = '/%s' % int(_id)
    return atmosphere.tools.create_req(method=atmosphere.tools.HTTP_DELETE, url=url)
