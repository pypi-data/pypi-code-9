import atmosphere.config
import atmosphere.tools

__author__ = 'paoolo'

PREFIX = '/compute_sites'


def get_all_compute_sites():
    """
    Get a list of registered compute sites.

    :return:
    """
    return atmosphere.tools.create_req()


def get_compute_sites(_id):
    """
    Get all details of a compute site.

    :param _id: positive decimal number, ID of a compute site (required)
    :return:
    """
    url = '/%s' % str(_id)
    return atmosphere.tools.create_req(url=url)
