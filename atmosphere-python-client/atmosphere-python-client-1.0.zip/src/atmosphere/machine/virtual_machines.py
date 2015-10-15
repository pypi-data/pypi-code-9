import atmosphere.tools

__author__ = 'paoolo'

PREFIX = '/virtual_machines'


def get_all_virtual_machines(app_id=None):
    """
    Get a list of virtual machines used by appliances added to user appliance sets.

    :param app_id: positive decimal number (optional)
    :return:
    """
    url = ''
    if app_id is not None:
        url += 'appliance_id=%s' % str(app_id)
    if len(url) > 0:
        url = '?' + url
    return atmosphere.tools.create_req(url=url)


def get_virtual_machines(_id):
    """
    Get all details of a virtual machine.

    :param _id: positive decimal number (optional)
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(url=url)
