# -*- coding: utf-8 -*-
#
# File: validators.py
#
# Copyright (c) nexiles GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import os
import re
import logging
import urlparse
import argparse


from nexiles.tools.api import pluralize

logger = logging.getLogger("nexiles.tools.meta")


OR_REGEX = re.compile("(OR|VR):(.*):(\d+)")

ALL_RESOURCES = """cabinets documents epmdocuments folders groups libraries
    organizations parts products projects reports teams types
    users workpackages""".split()

__all__ = ["is_url", "is_oid", "is_file_path"]


def is_url(string):
    """is_url(s) -> str

    Validates s to be a url.

    Raises `argparse.AttributeError` if a validation error occurs.

    :param s:  the string to check
    """
    scheme, netloc, path, query, fragment = urlparse.urlsplit(string)
    if not scheme:
        raise argparse.ArgumentTypeError("'%s' does not look like an URL." % string)
    if query or fragment:
        raise argparse.ArgumentTypeError("'%s' contains query args or a fragment part -- please remove these." % string)
    return string


def is_oid(oid):
    """is_oid(s) -> str

    Validates s to be a valid OID.

    Raises `argparse.AttributeError` if a validation error occurs.

    :param oid:  the string to check
    """
    oid = oid.replace("%3A", ":")  # allow URL pasted OIDs
    m = OR_REGEX.match(oid)
    if not m:
        raise argparse.ArgumentTypeError("'%s' is not a valid OID." % oid)
    return oid


def is_file_path(f):
    """is_file_path(s) -> path

    Validates s to be a valid file.

    This also expands the user's home directory, and normalizes case
    and path separators.

    Only **files** pass the check, and they *MUST* exist.

    Raises `argparse.AttributeError` if a validation error occurs.

    :param f:  the string to check
    """
    f = os.path.expanduser(f)
    f = os.path.normcase(f)
    f = os.path.normpath(f)

    if not os.path.exists(f):
        raise argparse.ArgumentTypeError("File '%s' does not exist" % f)

    if not os.path.isfile(f):
        raise argparse.ArgumentTypeError("File '%s' is not a regular file." % f)

    logger.debug("is_file_path: => %s" % f)
    return f


def is_resource(*args):
    """is_resource(*args) -> function

    Returns a validator function which validates a bassed in resource name
    against the given spec.

    If no spec is given, or "all" is given as a spec, then all *valid*
    resource names pass.

    :param args: the validation spec.

    :returns: validator function
    """

    if not args or args[0] == "all":
        def all_validator(s):
            if pluralize(s) not in ALL_RESOURCES:
                raise argparse.ArgumentTypeError("Resource '%s' not valid. Valid resources: %r" % (s, ALL_RESOURCES))
            return pluralize(s)
        return all_validator
    else:
        valid_resources = set(map(pluralize, args))

        def some_validator(s):
            if pluralize(s) not in ALL_RESOURCES:
                raise argparse.ArgumentTypeError("Resource '%s' not valid. Valid resources: %r" % (s, ALL_RESOURCES))

            if pluralize(s) not in valid_resources:
                raise argparse.ArgumentTypeError("Resource '%s' not valid. Valid resources: %r" % (s, valid_resources))
            return pluralize(s)
        return some_validator


def is_bool(s):
    """is_bool(s) -> bool

    Validates s to be a valid boolean.

    The string is deemed to be truthy iff it starts with one of:

        truthy ::= 'yes' | 'YES' | 'on' | 'ON' | '1' | 'true' | 'True'

    else it is deemed falsy.

    Raises `argparse.AttributeError` if a validation error occurs.

    :param s:  the string to check
    """
    if len(s):
        if s.upper() in ('YES', 'TRUE', 'ON', '1'):
            return True
    return False


# vim: set ft=python ts=4 sw=4 expandtab :
