# -*- coding: utf-8 -*-
#
# File: __init__.py
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'


import logging

from nexiles.tools.api import slumber

logger = logging.getLogger("nexiles.tools.api")


__all__ = ["get_api", "get_service", "get_root_api", "pluralize", "get_resource"]


is_singular = lambda x: not x.endswith("s")

SERVICE_TYPES = ["apps"]


def pluralize(x):
    if is_singular(x):
        return x + "s"
    return x


def get_resource(api, resource_type):
    """get_resource(api, resource_type) -> resource

    Returns a resource object for the given resource string.

    :param api:             The API object -- see :py:func:`get_api`
    :param resource_type:   The resource type string -- see :ref:`resources`

    :returns: resource
    """
    if is_singular(resource_type):
        resource_type = pluralize(resource_type)

    # switch to service url
    if resource_type in SERVICE_TYPES:
        api.to_service_url()
        logger.info("Service detected -> switching to service url (%s)" % api.get_url())

    return getattr(api, resource_type)


def get_root_api(base_url, username=None, password=None):
    """get_root_api(base_url, username, password) -> api

    Initializes and returns a new client API object.

    :param base_url:    the base URL, e.g. the `Windchill` App root
    :param username:    the user name
    :param password:    the password

    :returns:  New API object
    """
    logging.info("get_root_api: base_url=%s" % base_url)
    api_url = "/".join([base_url, "servlet", "nexiles", "tools"])
    logging.debug("get_api: api_url=%s" % api_url)
    return slumber.API(api_url, auth=(username, password), append_slash=False)


def get_api(base_url, username=None, password=None):
    """get_api(base_url, username, password) -> api

    Initializes and returns a new client API object.

    :param base_url:    the base URL, e.g. the `Windchill` App root
    :param username:    the user name
    :param password:    the password

    :returns:  New API object
    """
    logging.info("get_api: base_url=%s" % base_url)
    api_url = "/".join([base_url, "servlet", "nexiles", "tools", "api", "1.0"])
    logging.debug("get_api: api_url=%s" % api_url)
    return slumber.API(api_url, auth=(username, password), append_slash=False)


def get_service(base_url, service, username=None, password=None):
    """get_service(base_url, service, username, password) -> api

    Initializes and returns a new client service object.

    :param base_url:    the base URL, e.g. the `Windchill` App root
    :param service:     the service name
    :param username:    the user name
    :param password:    the password

    :returns:  New API object
    """
    logging.info("get_service: base_url=%s" % base_url)
    api_url = "/".join([base_url, "servlet", "nexiles", "tools", "services"])
    logging.debug("get_service: api_url=%s" % api_url)
    base = slumber.API(api_url, auth=(username, password), append_slash=False)
    return getattr(base, service)
