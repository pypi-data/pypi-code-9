# -*- coding: utf-8 -*-
#
# File: version.py
#
# Copyright (c) nexiles GmbH

__author__ = """Ramon Bartl <rb@nexiles.de>"""
__docformat__ = 'plaintext'

import logging
import pkg_resources

from nexiles.tools.api import get_root_api

logger = logging.getLogger("nexiles.tools.api")


class Version(object):
    """ Client/Server version wrapper
    """

    def __init__(self, base_url, username, password):
        self.api = get_root_api(base_url, username, password)

    def get_server_version(self):
        """get_server_version() -> version dict

        Performs a request to gather the server side version information

        :returns: version dict
        """
        version = {"version": "UNKNOWN",
                   "build"  : "UNKNOWN",
                   "date"   : "UNKNOWN"}
        version.update(self.api.version.get())
        return version

    def server_version(self):
        """server_version() -> version string

        Prints the version information into a single line string

        :returns: server version
        """
        return "version: %(version)s " \
               "build: %(build)s " \
               "date: %(date)s " % self.get_server_version()

    def client_version(self):
        """client_version() -> version string

        Uses the package resources to gather the version information

        :returns: client version
        """
        package = pkg_resources.get_distribution("nexiles.tools.api")
        return package.version


######################################################################
######################################################################
######################################################################


def command_version(api, args):
    version = Version(args.url, args.username, args.password)

    if args.server_version:
        print version.server_version()
    elif args.client_version:
        print version.client_version()
    else:
        print "nexiles.tools version: %s" % version.server_version()
        print "nexiles.tools.api version: %s" % version.client_version()

def add_commands(subparsers, defaults):
    subparser = subparsers.add_parser("version")

    subparser.add_argument("--server-version", dest="server_version", action="store_true")
    subparser.add_argument("--client-version", dest="client_version", action="store_true")

    subparser.set_defaults(command=command_version)

# vim: set ft=python ts=4 sw=4 expandtab :
