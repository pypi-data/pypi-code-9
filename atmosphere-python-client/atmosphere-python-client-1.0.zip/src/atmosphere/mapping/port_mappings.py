import atmosphere.tools

__author__ = 'paoolo'

PREFIX = '/port_mappings'


def get_all_port_mappings(_all=False, port_mapping_template_id=None, virtual_machine_id=None):
    """
    Get a list of port mappings.

    :param port_mapping_template_id:
    :param virtual_machine_id:
    :return:
    """
    url = 'all=true' if _all else ''
    if port_mapping_template_id is not None:
        url += 'port_mapping_template_id=%s' % str(port_mapping_template_id)
    if virtual_machine_id is not None:
        if len(url) > 0:
            url += '&'
        url += 'virtual_machine_id=%s' % str(virtual_machine_id)
    if len(url) > 0:
        url = '?' + url
    return atmosphere.tools.create_req(url=url)


def get_port_mapping(_id):
    """
    Get all details of a port mapping.

    :param _id:
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(url=url)
