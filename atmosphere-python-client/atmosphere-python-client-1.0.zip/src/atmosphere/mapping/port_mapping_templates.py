import atmosphere.tools

__author__ = 'paoolo'

PREFIX = '/port_mapping_templates'


def get_all_port_map_temp_by_at(appliance_type_id):
    """
    Get all port mapping template for given appliance type.

    :param appliance_type_id: positive decimal number, ID of appliance type (required)
    :return:
    """
    url = '?appliance_type_id=%s' % str(appliance_type_id)
    return atmosphere.tools.create_req(url=url)


def get_all_port_map_temp_by_dev(dev_mode_property_set_id, target_port=None):
    """
    Get all port mapping template for given dev mode property set.

    :param dev_mode_property_set_id: positive decimal number, ID of dev mode property set (required)
    :param target_port:
    :return:
    """
    url = '?dev_mode_property_set_id=%s' % str(dev_mode_property_set_id)
    if target_port is not None:
        url += '&target_port=%s' % str(target_port)
    return atmosphere.tools.create_req(url=url)


def get_port_map_temp(_id):
    """
    Get port mapping template description.

    :param _id: positive decimal number, ID of port mapping template (required)
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(url=url)


def create_port_map_temp_for_at(appliance_type_id,
                                transport_protocol, application_protocol, service_name, target_port):
    """
    Create port mapping template for appliance type.

    :param appliance_type_id: positive decimal number, ID of appliance type (required)
    :param transport_protocol: one of "tcp" or "udp" (required)
    :param application_protocol: one of "http", "https", "http_https", "none" (required)
    :param service_name: any string (required)
    :param target_port: positive decimal number, port number (required)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    body = {'port_mapping_template': _data}
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_POST, body=body)


def create_port_map_temp_for_dev(dev_mode_property_set_id,
                                 transport_protocol, application_protocol, service_name, target_port):
    """

    :param dev_mode_property_set_id: positive decimal number, ID of dev mode property set (required)
    :param transport_protocol: one of "tcp" or "udp" (required)
    :param application_protocol: one of "http", "https", "http_https", "none" (required)
    :param service_name: any string (required)
    :param target_port: positive decimal number, port number (required)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    body = {'port_mapping_template': _data}
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_POST, body=body)


def update_port_map_temp(_id, appliance_type_id=None, dev_mode_property_set_id=None,
                         transport_protocol=None, application_protocol=None, service_name=None, target_port=None):
    """
    Update port mapping template.

    :param _id: positive decimal number, ID of port mapping template (required)
    :param appliance_type_id: positive decimal number, ID of appliance type (optional)
    :param dev_mode_property_set_id: positive decimal number, ID of dev mode property set (optional)
    :param transport_protocol: one of "tcp" or "udp" (optional)
    :param application_protocol: one of "http", "https", "http_https", "none" (optional)
    :param service_name: any string (optional)
    :param target_port: positive decimal number, port number (optional)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    _data['id'] = _id
    body = {'port_mapping_template': _data}
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_PUT, url=url, body=body)


def delete_port_map_temp(_id):
    """
    Delete port mapping template.

    :param _id: positive decimal number, ID of port mapping template (required)
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(method=atmosphere.tools.HTTP_DELETE, url=url)


def get_dev_id_for_app(app_id, dev_sets):
    if 'dev_mode_property_sets' in dev_sets:
        for dev_set in dev_sets['dev_mode_property_sets']:
            if 'appliance_id' in dev_set and dev_set['appliance_id'] == app_id:
                return dev_set
    return None
