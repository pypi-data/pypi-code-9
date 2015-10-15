import atmosphere.tools

__author__ = 'paoolo'

PREFIX = '/http_mappings'


def get_all_http_map(app_id=None, port_mapping_template_id=None):
    """
    Get a list of http mappings.

    :param app_id:
    :param port_mapping_template_id:
    :return:
    """
    url = ''
    if app_id is not None:
        url += 'appliance_id=%s' % str(app_id)
    if port_mapping_template_id is not None:
        if len(url) > 0:
            url += '&'
        url += 'port_mapping_template_id=%s' % str(port_mapping_template_id)
    if len(url) > 0:
        url = '?' + url
    return atmosphere.tools.create_req(url=url)


def get_http_map(_id):
    """
    Get all details of a http mapping.

    :param _id:
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(url=url)
