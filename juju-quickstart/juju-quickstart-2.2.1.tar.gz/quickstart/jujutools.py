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

"""Quickstart utility functions for managing Juju environments and entities."""

from __future__ import unicode_literals

from quickstart import (
    jujugui,
    serializers,
    settings,
)


def get_api_url(
        api_address, juju_version, env_uuid,
        path_prefix='', charm_ref=None, insecure=False):
    """Return the Juju WebSocket API endpoint.

    Receives the Juju API server address, the Juju version and the unique
    identifier of the current environment.

    Optionally a prefix to be used in the path and a flag indicating whether
    to use secure or insecure WebSockets.

    Optionally also receive the Juju GUI charm reference as an instance of
    "jujubundlelib.references.Reference". If provided, the function checks that
    the corresponding Juju GUI charm supports the new Juju API endpoint.
    If not supported, the old endpoint is returned.

    The environment UUID can be None, in which case the old-style API URL
    (not including the environment UUID) is returned.
    """
    schema = 'ws' if insecure else 'wss'
    base_url = '{}://{}'.format(schema, api_address)
    path_prefix = path_prefix.strip('/')
    if path_prefix:
        base_url = '{}/{}'.format(base_url, path_prefix)
    if (env_uuid is None) or (juju_version < (1, 22, 0)):
        return base_url
    complete_url = '{}/environment/{}/api'.format(base_url, env_uuid)
    if charm_ref is None:
        return complete_url
    # If a customized Juju GUI charm is in use, there is no way to check if the
    # GUI server is recent enough to support the new Juju API endpoints.
    # In these cases, assume the customized charm is recent enough.
    if not jujugui.is_promulgated(charm_ref):
        return complete_url
    # This is the promulgated Juju GUI charm. Check if it supports new APIs.
    revision, series = charm_ref.revision, charm_ref.series
    if revision < settings.MINIMUM_REVISIONS_FOR_NEW_API_ENDPOINT[series]:
        return base_url
    return complete_url


def get_service_info(status, service_name):
    """Retrieve information on the given service and on its first alive unit.

    Return a tuple containing two values: (service data, unit data).
    Each value can be:
        - a dictionary of data about the given entity (service or unit) as
          returned by the Juju watcher;
        - None, if the entity is not present in the Juju environment.
    If the service data is None, the unit data is always None.
    """
    services = [
        data for entity, action, data in status if
        (entity == 'service') and (action != 'remove') and
        (data['Name'] == service_name) and (data['Life'] == 'alive')
    ]
    if not services:
        return None, None
    units = [
        data for entity, action, data in status if
        entity == 'unit' and action != 'remove' and
        data['Service'] == service_name
    ]
    return services[0], units[0] if units else None


def parse_status_output(output, keys=None):
    """Parse the output of juju status.

    Return selection specified by the keys array.
    Raise a ValueError if the selection cannot be retrieved.
    """
    if keys is None:
        keys = ['dummy']
    try:
        status = serializers.yaml_load(output)
    except Exception as err:
        raise ValueError(b'unable to parse the output: {}'.format(err))

    selection = status
    for key in keys:
        try:
            selection = selection.get(key, {})
        except AttributeError as err:
            msg = 'invalid YAML contents: {}'.format(status)
            raise ValueError(msg.encode('utf-8'))
    if selection == {}:
        msg = '{} not found in {}'.format(':'.join(keys), status)
        raise ValueError(msg.encode('utf-8'))
    return selection


def get_agent_state(output):
    """Parse the output of juju status for the agent state.

    Return the agent state.
    Raise a ValueError if the agent state cannot be retrieved.
    """
    return parse_status_output(output, ['machines', '0', 'agent-state'])


def get_bootstrap_node_series(output):
    """Parse the output of juju status for the agent state.

    Return the agent state.
    Raise a ValueError if the agent state cannot be retrieved.
    """
    return parse_status_output(output, ['machines', '0', 'series'])
