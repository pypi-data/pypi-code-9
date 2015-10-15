import atmosphere.tools

__author__ = 'paoolo'

PREFIX = '/virtual_machine_templates'


def get_all_virtual_machines_templates(_all=False):
    """
    Get a list of virtual machines used by appliances added to user appliance sets.

    :return:
    """
    url = '?all=true' if _all else ''
    return atmosphere.tools.create_req(url=url)
