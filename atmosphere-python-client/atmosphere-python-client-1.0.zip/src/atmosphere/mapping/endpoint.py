import atmosphere.tools

__author__ = 'paoolo'

PREFIX = '/endpoints'


def get_all_endpoints():
    """
    Get a list of endpoints defined for a given port mapping template.

    :return:
    """
    return atmosphere.tools.create_req()


def get_endpoint(_id):
    """
    Get the full JSON document about a given endpoint.

    :param _id: positive decimal number, ID of endpoint (required)
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(url=url)


def create_endpoint(port_mapping_template_id, name=None,
                    description=None, descriptor=None,
                    endpoint_type=None, invocation_path=None,
                    secured=None):
    """
    Creates a new endpoint.

    :param port_mapping_template_id: positive decimal number, ID of the port mapping template (required)
    :param name: any string, short name (required)
    :param description: any string, long textual human-readable description (optional)
    :param descriptor: any string, machine-readable (optional)
    :param endpoint_type: one of "rest", "ws", "webapp" (required)
    :param invocation_path: any string, app invocation path (required)
    :param secured: if endpoint is secured (optional, default False)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    body = {'endpoint': _data}
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_POST, body=body)


def update_endpoint(_id, port_mapping_template_id=None, name=None,
                    description=None, descriptor=None,
                    endpoint_type=None, invocation_path=None,
                    secured=None):
    """
    Update endpoint.

    :param _id: positive decimal number, ID of endpoint (required)
    :param port_mapping_template_id: positive decimal number, ID of the port mapping template (required)
    :param name: any string, short name (required)
    :param description: any string, long textual human-readable description (optional)
    :param descriptor: any string, machine-readable (optional)
    :param endpoint_type: one of "rest", "ws", "webapp" (required)
    :param invocation_path: any string, app invocation path (required)
    :param secured: if endpoint is secured (optional, default False)
    :return:
    """
    _data = atmosphere.tools.get_data(locals())
    _data['id'] = _id
    body = {'endpoint': _data}
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req_json_body(method=atmosphere.tools.HTTP_POST, url=url, body=body)


def delete_endpoint(_id):
    """
    Delete endpoint.

    :param _id: positive decimal number, ID of endpoint (required)
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(method=atmosphere.tools.HTTP_DELETE, url=url)


def get_endpoint_descriptor(_id):
    """
    Get descriptor of endpoint.

    :param _id: positive decimal number, ID of endpoint (required)
    :return:
    """
    url = '/%s/descriptor' % str(_id)
    return atmosphere.tools.create_req(method=atmosphere.tools.HTTP_GET, url=url)
