# -*- coding: utf-8 -*-
#
# File: query.py
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'

import logging

from nexiles.tools.api import validators
from nexiles.tools.api import get_resource
from nexiles.tools.api import utils

logger = logging.getLogger("nexiles.tools.api")


def query(api, type=None, **kw):
    """query(api, type, ...) -> result

    Perform a query.

    :param api:    The resource -- see :py:func:`nexiles.tools.api.get_api`
    :param type:   The resource type string -- see :ref:`resources`

    :returns: query result
    """
    if type is None:
        type = "document"  # XXX: defaults system

    resource = get_resource(api, type)
    return utils.query(resource, **kw)


def query_one(api, type=None, key_func=None, **kw):
    """query_one(api, type, ...) -> result

    Perform a query, return only **one** result.

    This function uses :py:func:`nexiles.tools.api.query` internally.  It sorts
    the result set returned by that function using the given function as the
    `key` argument for the python `sorted()` builtin.

    The default key function used is one that sorts the results by **sequence
    numbers** -- i.e. the number pert of the **OID**.  Please note that this
    might be considered as a hack.

    .. note:: The **first** element of the result set **after** sorting is returned.

    :param api:         The resource -- see :py:func:`nexiles.tools.api.get_api`
    :param type:        The resource type string -- see :ref:`resources`
    :param key_func:    The key function to use for the sort.
    :param kw:          The query arguments

    :returns: query result
    """
    kw["latest_iteration"] = True
    results = query(api, type=type, **kw)

    if key_func is None:
        key_func = lambda item: -long(item["oid"].split(":")[2])

    if len(results):
        return sorted(results, key=key_func)[0]

    return None


######################################################################
######################################################################
######################################################################


def command_query(api, args):
    verbose = args.verbose == True
    resource = get_resource(api, args.type)

    query = {
        "limit": args.limit
    }

    if args.name:
        query["name"] = args.name

    if args.number:
        query["number"] = args.number

    if args.state:
        query["state"] = args.state

    if args.latest_iteration is False:
        query["latest_iteration"] = "no"

    if args.latest_iteration is True:
        query["latest_iteration"] = "yes"

    if args.latest_released:
        query["latest_released"] = "yes"

    logger.debug("query: %r" % query)

    results = utils.query(resource, **query)

    print "%d results" % len(results)
    for nr, item in enumerate(results):
        if nr == 0:
            if verbose:
                print "%-4s %-35s %-30s %-12s %-6s" % ("nr", "name", "OID", "state", "version")
                print "-" * 92
            else:
                print "%-4s %-35s %-30s" % ("nr", "name", "OID")
                print "-" * 75
        print "%03d:" % nr,  "%(name)-35s %(oid)-30s" % item,
        if verbose:
            object_details = utils.get_object(resource, item["oid"])
            print "%(state)-12s %(version)-6s" % object_details.item,
        print


def add_commands(subparsers, defaults):
    subparser = subparsers.add_parser("list")
    subparser.add_argument("--name", dest="name", type=str)
    subparser.add_argument("--number", dest="number", type=str)
    subparser.add_argument("--type", dest="type", default=defaults.default_type, type=validators.is_resource("all"))
    subparser.add_argument("--limit", dest="limit", default=100, type=int)
    subparser.add_argument("--state", dest="state", type=str)
    subparser.add_argument("--latest-released", dest="latest_released", action="store_true")
    subparser.add_argument("--latest-iteration", dest="latest_iteration", type=validators.is_bool)
    subparser.set_defaults(command=command_query)

# vim: set ft=python ts=4 sw=4 expandtab :
