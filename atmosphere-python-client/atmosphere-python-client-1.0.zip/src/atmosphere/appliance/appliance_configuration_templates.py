import atmosphere.tools

__author__ = 'paoolo'

PREFIX = '/appliance_configuration_templates'


def get_all_app_config_temp():
    """
    Get list of all available appliance configuration templates.

    :return: list of appliance configuration templates
    """
    return atmosphere.tools.create_req()


def create_app_conf_temp(appliance_type_id, name=None, payload=None):
    """
    Create a new appliance configuration template.

    :param appliance_type_id: positive decimal number (required)
    :param name: any string (optional)
    :param payload: any string (optional)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    body = {'appliance_configuration_template': _data}
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_POST, body=body)


def update_app_conf_temp(_id, name=None, payload=None):
    """
    Update appliance configuration template.

    :param _id: positive decimal number (required)
    :param name: any string (optional)
    :param payload: any string (optional)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    _data['id'] = _id
    body = {'appliance_configuration_template': _data}
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_PUT, url=url, body=body)


def delete_app_conf_temp(_id):
    """
    Delete appliance configuration template.

    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(method=atmosphere.tools.HTTP_DELETE, url=url)