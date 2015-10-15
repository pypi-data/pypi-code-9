import atmosphere.tools


__author__ = 'paoolo'

PREFIX = '/appliance_sets'


def get_all_app_set():
    """
    Get list of all appliance sets.

    :return: list of all appliance sets
    """
    return atmosphere.tools.create_req()


def get_app_set(_id):
    """
    Get info about selected appliance set.

    :param _id: positive decimal number, ID of appliance set (required)
    :return: information about appliance set
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(url=url)


APP_SET_TYPE_DEV = 'development'
APP_SET_TYPE_PORTAL = 'portal'
APP_SET_TYPE_WORKFLOW = 'workflow'


def create_app_set(name=None, priority=None, appliance_set_type=None):
    """
    Create appliance set.

    :param name: any string (optional)
    :param priority: positive decimal number (optional)
    :param appliance_set_type: select one of appliance_sets.APP_SET_TYPE_* (optional, default: "workflow")
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    body = {'appliance_set': _data}
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_POST, body=body)


def update_app_set(_id, name=None, priority=None):
    """
    Update information of appliance set.

    :param _id: positive decimal number (required)
    :param name: any string (optional)
    :param priority: positive decimal number (optional)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    _data['id'] = _id
    body = {'appliance_set': _data}
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_PUT, url=url, body=body)


def delete_app_set(_id):
    """
    Delete appliance set.

    :param _id: positive decimal number (required)
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(method=atmosphere.tools.HTTP_DELETE, url=url)