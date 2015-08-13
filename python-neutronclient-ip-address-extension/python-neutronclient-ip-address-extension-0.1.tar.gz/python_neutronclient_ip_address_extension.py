# Copyright 2015 Rackspace Hosting Inc.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

from neutronclient.common import extension
from neutronclient.i18n import _
from neutronclient.neutron import v2_0 as neutronV20


class IPAddress(extension.NeutronClientExtension):
    resource = 'ip_address'
    resource_plural = '%ses' % resource
    object_path = '/%s' % resource_plural
    resource_path = '/%s/%%s' % resource_plural
    versions = ['2.0']

    allow_names = False
    list_columns = ['id', 'address', 'version', 'address_type', 'network_id',
                    'subnet_id', 'port_ids']


class IPAddressesList(extension.ClientExtensionList, IPAddress):
    """List all IP addresses."""
    shell_command = 'ip-address-list'


class IPAddressesCreate(extension.ClientExtensionCreate, IPAddress):
    """Create an IP address."""
    shell_command = 'ip-address-create'

    def add_known_arguments(self, parser):
        parser.add_argument(
            'network_id', metavar='NETWORK_ID',
            help=_('Network ID this IP address belongs to.'))
        parser.add_argument(
            'version',
            type=int, metavar='IP_VERSION',
            help=_('IP version to use, e.g 4 or 6.'))
        parser.add_argument(
            '--port-id',
            help=_('Port ID this IP address associates with.'),
            action='append')
        parser.add_argument(
            '--device-id',
            help=_('Device ID this IP address associates with.'),
            action='append')

    def args2body(self, parsed_args):
        body = {}
        if parsed_args.version:
            body['version'] = parsed_args.version
        if parsed_args.network_id:
            body['network_id'] = parsed_args.network_id
        if parsed_args.port_id:
            body['port_ids'] = parsed_args.port_id
        if parsed_args.device_id:
            body['device_ids'] = parsed_args.device_id
        neutronV20.update_dict(parsed_args, body, [])
        return {self.resource: body}


class IPAddressesUpdate(extension.ClientExtensionUpdate, IPAddress):
    """Update an IP address."""
    shell_command = 'ip-address-update'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--port-id',
            help=_('Port ID this IP address associates with.'),
            action='append')

    def args2body(self, parsed_args):
        body = {}
        if parsed_args.port_id:
            body['port_ids'] = parsed_args.port_id
        neutronV20.update_dict(parsed_args, body, [])
        return {self.resource: body}


class IPAddressesDelete(extension.ClientExtensionDelete, IPAddress):
    """Delete an IP address."""
    shell_command = 'ip-address-delete'


class IPAddressesShow(extension.ClientExtensionShow, IPAddress):
    """Show an IP address."""
    shell_command = 'ip-address-show'


class IPAddressesPorts(extension.NeutronClientExtension):
    parent_resource = 'ip_addresses'
    child_resource = 'port'
    resource = '%s_%s' % (parent_resource, child_resource)
    resource_plural = '%ss' % resource
    child_resource_plural = '%ss' % child_resource
    object_path = '/%s/%%s/%s' % (parent_resource, child_resource_plural)
    resource_path = '/%s/%%s/%s/%%%%s' % (
        parent_resource, child_resource_plural)
    versions = ['2.0']


class IPAddressesPortsList(extension.ClientExtensionList, IPAddressesPorts):
    pass


class IPAddressesPortsUpdate(extension.ClientExtensionUpdate,
                             IPAddressesPorts):
    pass
