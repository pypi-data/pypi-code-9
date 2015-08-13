# This file is part of the Juju Quickstart Plugin, which lets users set up a
# Juju environment in very few steps (https://launchpad.net/juju-quickstart).
# Copyright (C) 2015 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License version 3, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Quickstart helpers for working with the Juju GUI charm and service."""

from __future__ import (
    print_function,
    unicode_literals,
)

import logging

from jujubundlelib import references

from quickstart import settings


def add_tokens_to_url(url, auth_token, changes_token):
    """Return an URL including the optional authentication and changes tokens.

    If auth_token and changes_token are both None, the given URL is returned
    without changes.
    """
    query = []
    if auth_token is not None:
        query.append('authtoken=' + auth_token)
    if changes_token is not None:
        query.append('changestoken=' + changes_token)
    if query:
        return '{}/?{}'.format(url, '&'.join(query))
    return url


def build_options(port, source):
    """Create a configuration dict suitable to be used when deploying the GUI.

    Return None if no customized options are present.
    """
    options = {}
    if port is not None:
        options['port'] = port
    if source is not None:
        user, branch = source
        value = 'https://github.com/{}/juju-gui.git {}'.format(user, branch)
        options['juju-gui-source'] = value
    return options or None


def is_promulgated(reference):
    """Report whether the given reference represents a GUI promulgated charm.

    The given reference is an instance of "jujubundlelib.references.Reference".
    """
    return (
        reference.name == settings.JUJU_GUI_CHARM_NAME and
        not reference.user and
        not reference.is_local()
    )


def normalize_config(options):
    """Normalize the Juju GUI configuration options.

    For instance, set the default port if none is set in the given options.
    """
    options = options.copy()
    if not options['secure']:
        logging.warn('the Juju GUI is running in insecure mode')
    if options['port'] is None:
        options['port'] = 443
    return options


def parse_charm_url(charm_url):
    """Parse the given charm URL.

    Check if the charm URL seems to refer to a Juju GUI charm.
    Print (to stdout or to logs) info and warnings about the charm URL.

    Return the parsed charm reference object as an instance of
    "jujubundlelib.references.Reference".
    """
    print('charm URL: {}'.format(charm_url))
    ref = references.Reference.from_fully_qualified_url(charm_url)
    charm_name = settings.JUJU_GUI_CHARM_NAME
    if ref.name != charm_name:
        # This does not seem to be a Juju GUI charm.
        logging.warn(
            'unexpected URL for the {} charm: '
            'the service may not work as expected'.format(charm_name))
        return ref
    if ref.user or ref.is_local():
        # This is not the official Juju GUI charm.
        logging.warn('using a customized {} charm'.format(charm_name))
    elif ref.revision < settings.MINIMUM_REVISIONS_FOR_BUNDLES[ref.series]:
        # This is the official Juju GUI charm, but it is outdated.
        logging.warn(
            'charm is outdated and may not support bundle deployments')
    return ref
