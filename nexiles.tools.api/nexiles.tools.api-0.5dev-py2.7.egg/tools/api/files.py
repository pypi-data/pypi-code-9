# -*- coding: utf-8 -*-
#
# File: query.py
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'

import sys
import logging

from nexiles.tools.api import validators
from nexiles.tools.api import get_resource
from nexiles.tools.api import get_service
from nexiles.tools.api import utils
from nexiles.tools.api import query

logger = logging.getLogger("nexiles.tools.api")

def fileservice(base_url, username, password):
    """fileservice(base_url, username, password) -> file service object

    Returns file service object.

    :param base_url:   the windchill base url
    :param username:   the user name to use for authentication
    :param password:   the password to use for authentication
    :returns:          file service object
    """
    return get_service(base_url, "files", username, password=password)


def fetch(service, number, filename):
    """fetch(service, number, filename) -> result

    Uses the file service to fetch a file, returns the file content.

    :param service:     The file service object
    :param number:      The number of the document

    :returns:           file content
    """
    return service(number)(filename).get(__raw__=True)



######################################################################
######################################################################
######################################################################

def get_number(api, name):
    results = query.query(api, name=name)
    if len(results):
        if len(results) != 1:
            for nr, res in enumerate(results):
                print >>sys.stderr, "%03d: %r" % (nr, res)
            utils.die(10, "file-fetch: query for name '%s' returned more than one result." % name)

        return results[0]["number"]
    else:
        utils.die(10, "file-fetch: query for name '%s' returned no results." % name)


def check_number(api, number):
    results = query.query(api, number=number)
    return len(results) == 1

def command_fetch(api, args):
    verbose = args.verbose == True
    service = fileservice(args.url, username=args.username, password=args.password)

    number = args.number
    if args.name:
        number = get_number(api, args.name)

    if not check_number(api, number):
        utils.die(10, "file-fetch: No document with number '%s' found." % number)

    logger.debug("file-fetch: number=%s filename=%s" % (args.number, args.filename))

    destination_file = args.filename
    if args.destination:
        destination_file = args.destination

    with file(destination_file, "wb") as f:
        f.write(fetch(service, number, args.filename))

def add_commands(subparsers, defaults):
    subparser = subparsers.add_parser("file-fetch")
    subparser.add_argument("--name", help="the name of the document", dest="name", type=str)
    subparser.add_argument("--number", help="the number of the document", dest="number", type=str)
    subparser.add_argument("--filename", help="the name of the file to download", dest="filename", type=str)
    subparser.add_argument("--destination", help="the name of the local file", required=False, dest="destination", type=str)
    subparser.set_defaults(command=command_fetch)

# vim: set ft=python ts=4 sw=4 expandtab :
