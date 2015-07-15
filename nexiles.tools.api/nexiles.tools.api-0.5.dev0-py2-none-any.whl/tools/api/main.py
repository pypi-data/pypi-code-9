# -*- coding: utf-8 -*-
#
# File: __init__.py
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'

import sys
import logging
import argparse

from nexiles.tools.api import get_api
from nexiles.tools.api import log
from nexiles.tools.api import validators

from nexiles.tools.api.defaults import get_defaults

logger = logging.getLogger("nexiles.tools.api")

from nexiles.tools.api import query
from nexiles.tools.api import content
from nexiles.tools.api import checkinout
from nexiles.tools.api import document
from nexiles.tools.api import apps
from nexiles.tools.api import version
from nexiles.tools.api import serve
from nexiles.tools.api import files

__all__ = ["main"]


class VersionAction(argparse._VersionAction):
    def __call__(self, parser, namespace, values, option_string=None):
        args = namespace
        v = version.Version(args.url, args.username, args.password)
        server_version = v.server_version()
        formatter = parser._get_formatter()
        formatter.add_text(server_version)
        parser.exit(message=formatter.format_help())


class SurfDirectory(argparse._VersionAction):
    def __call__(self, parser, namespace, values, option_string=None):
        args = namespace
        print args.surf


def main():
    defaults = get_defaults()

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", dest="loglevel", action="store_const", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument("-l", "--logfile", default=defaults.logfile, type=str)
    parser.add_argument("-u", "--username", default=defaults.wt_username, help="the user name to use")
    parser.add_argument("-p", "--password", default=defaults.wt_pass, help="the password")
    parser.add_argument("-U", "--url", default=defaults.default_url, type=validators.is_url, help="windchill url")
    parser.add_argument("-X", "--post-mortem", dest="pdb", default=defaults.post_mortem, action="store_true", help="enable post-mortem pdb on exception")
    parser.add_argument("-v", "--verbose", dest="verbose", default=defaults.verbose, action="store_true", help="more verbose output -- causes more requests to be made.")
    parser.add_argument("-V", "--version", action=VersionAction, help="Print server side version and exit")

    subparsers = parser.add_subparsers()
    query.add_commands(subparsers, defaults)
    content.add_commands(subparsers, defaults)
    checkinout.add_commands(subparsers, defaults)
    document.add_commands(subparsers, defaults)
    apps.add_commands(subparsers, defaults)
    version.add_commands(subparsers, defaults)
    serve.add_commands(subparsers, defaults)
    files.add_commands(subparsers, defaults)

    args = parser.parse_args()

    if args.pdb:
        import traceback
        import pdb

        def debugger(type, value, tb):
            print >>sys.stderr, "*" * 70
            print >>sys.stderr, "unhandled exception:"
            traceback.print_exception(type, value, tb)
            print >>sys.stderr, "*" * 70
            print >>sys.stderr, "entering post-mortem debugger"
            pdb.pm()

        sys.excepthook = debugger

    log.setup_logging(level=args.loglevel, logfile=args.logfile)

    api = get_api(args.url, args.username, args.password)

    args.command(api, args)


if __name__ == '__main__':
    main()
