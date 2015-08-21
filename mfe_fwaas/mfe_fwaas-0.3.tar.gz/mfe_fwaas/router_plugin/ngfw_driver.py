# Copyright 2015 Intel Corporation.
#
# All Rights Reserved.
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

import os
import ngfw_smc_driver
import time
from eventlet import greenthread
from novaclient.v1_1 import client as novaclient
from oslo_config import cfg
from oslo_log import log as logging
from neutron.common import exceptions
from neutron.api.v2 import attributes
from neutron.extensions import l3
from neutron import manager
import json
import pprint
import pdb

LOG = logging.getLogger(__name__)

cfg.CONF.register_opts([
    cfg.StrOpt('tenant_admin_name', help="Name of tenant admin user"),
    cfg.StrOpt('tenant_admin_password', help='Tenant admin password'),
    cfg.StrOpt('tenant_id', help="Tenant UUID used to hold router instances"),
    cfg.StrOpt('tenant_name', help="Tenant name used to hold router instances"),
    cfg.StrOpt('ngfw_image_id', help="Sg-engine image UUID"),
    cfg.StrOpt('ngfw_mgmt_network_id', help="UUID of network connecting NGFW and SMC"),
    cfg.StrOpt('ngfw_flavor_id', help="Sg-engine flavor UUID"),
    cfg.IntOpt('vm_status_polling_interval', help="seconds between two polls of NGFW VM status"),
    cfg.IntOpt('vm_spawn_timeout', help="Timeout value to wait for VM spawn"),
    cfg.IntOpt('fw_status_polling_interval', help="seconds between two polls of single fw"),
    cfg.IntOpt('fw_status_polling_timeout', help="Timeout value to wait for single fw status polling"),
    cfg.StrOpt('smc_url', help="SMC server URL"),
    cfg.StrOpt('smc_api_version', help="SMC API version"),
    cfg.StrOpt('smc_api_auth_key', help="Authentication key to SMC API"),
    cfg.StrOpt('mac_address_prefix', help="The first 3 octets of ngfw MAC address")
    ],
    "NGFW")

class NgfwRouterDriver(object):

    def __init__(self):
        """
        Create Nova client handle
        """
        self._pp=pprint.PrettyPrinter()
        self._smc_ref = cfg.CONF.NGFW.smc_url + '/' + cfg.CONF.NGFW.smc_api_version + '/'
        
        self._smc_connection = ngfw_smc_driver.SMCAPIConnection(cfg.CONF.NGFW.smc_url,
                                                          cfg.CONF.NGFW.smc_api_version,
                                                          cfg.CONF.NGFW.smc_api_auth_key)
        
        self._novaclient = novaclient.Client(username=cfg.CONF.NGFW.tenant_admin_name,
                                             api_key=cfg.CONF.NGFW.tenant_admin_password,
                                             project_id=cfg.CONF.NGFW.tenant_name,
                                             auth_url=cfg.CONF.nova_admin_auth_url)

    @property
    def _core_plugin(self):
        return manager.NeutronManager.get_plugin()

    def _generate_mac_address(self, router_id, interface_id):
        return cfg.CONF.NGFW.mac_address_prefix + ":" + \
                        router_id[-4:-2] + ":" + \
                        router_id[-2:] + ":" + \
                        hex(int(interface_id))[2:]

    def create_router(self, context, router):
        """
        Bring up sg-engine VM
        """
        router_id = router['router']['id']
        router_name = 'ngfw_{0}'.format(router_id)
        mac_address = self._generate_mac_address(router_id, 0)
                
        # create a port on ngfw network and get its IP address
        mgmt_port = self._core_plugin.create_port(context.elevated(), {
                                'port': {'tenant_id': cfg.CONF.NGFW.tenant_id,
                                         'network_id': cfg.CONF.NGFW.ngfw_mgmt_network_id,
                                         'mac_address': mac_address,
                                         'fixed_ips': attributes.ATTR_NOT_SPECIFIED,
                                         'device_owner': '',
                                         'device_id': '',
                                         'admin_state_up': True,
                                         'name': ''}})
        print "XXXXXXXXXX"
        print router
        print "mgmt_port:"
        print mgmt_port
        filters = {'network_id': [cfg.CONF.NGFW.ngfw_mgmt_network_id]}
        print filters
        subnet = self._core_plugin.get_subnets(context.elevated(), filters)[0]
        mask = '/' + str(subnet['cidr']).split('/')[1]
        print "XXXXXXXXX"
        print subnet
        if not mgmt_port['fixed_ips']:
            raise Exception(_("Failed to create port on ngfw network for router {0}".format(router['router']['name'])))
        ngfw_manage_ip = str(mgmt_port['fixed_ips'][0]['ip_address']) + mask
        LOG.debug("Using IP address {0} as management IP for router {1}".format(ngfw_manage_ip, router['router']['name']))

        try:
            contact = ngfw_smc_driver.create_L3FW(router_name, ngfw_manage_ip)
        except:
            self._core_plugin.delete_port(context.elevated(), mgmt_port['id'], l3_port_check=False)
            raise
            
        # Get the ref to the newly declared single_fw
        # TODO: may need to gracefully handle smc exceptions
        router_ref = self._get_ngfw_ref(router_name)
        smc_connection = self._smc_connection

        # Prepare to create ngfw VM
        files = {'/config/base/cloud/engine.cfg' : contact}
        
        # ngfw requires at least one out-going interface other than the management interface!
        nics = [{'port-id' : mgmt_port['id']}]
#                {'net-id' : cfg.CONF.NGFW.ngfw_mgmt_network_id}]

        try:
            ngfw = self._novaclient.servers.create(name=router_name,
                                                   image=cfg.CONF.NGFW.ngfw_image_id,
                                                   flavor=cfg.CONF.NGFW.ngfw_flavor_id,
                                                   nics=nics,
                                                   files=files)
        except:
            LOG.error("Failed to create ngfw instance")
            self._core_plugin.delete_port(context.elevated(), mgmt_port['id'], l3_port_check=False)
            smc_connection.login()
            smc_connection.delete(router_ref)
            smc_connection.logout()
            raise

        def _vm_status(vm_id, vm_type):
            while True:
                try:
                    vm = self._novaclient.servers.get(vm_id)
                except:
                    LOG.error("Failed to get VM (id = {0}) status".format(vm_id))
                    raise

                LOG.debug("{0} {1} spawn status: {2}".format(vm_type, vm_id, vm.status))

                if vm.status not in ('ACTIVE', 'ERROR'):
                    yield cfg.CONF.NGFW.vm_status_polling_interval
                elif vm.status == 'ERROR':
                    raise VmStatusError(vm_type)
                else:
                    break
                
        try:
            self._wait(_vm_status, cfg.CONF.NGFW.vm_spawn_timeout, ngfw.id, 'ngfw')
        except:
            LOG.error("Failed to spawn ngfw id = {0}".format(ngfw.id))
            #self._novaclient.servers.delete(ngfw)
            self._core_plugin.delete_port(context.elevated(), mgmt_port['id'])
            smc_connection.login()
            smc_connection.delete(router_ref)
            smc_connection.logout()
            raise

        # verify ngfw's connection to SMC
        def _fw_status(router_ref, wait_for_status):
            smc_connection.login()
            while True:
                try:
                    result = smc_connection.get(router_ref)
                    fw_node_status_ref = None
                    fw_node_link_list = result[0]['nodes'][0]['firewall_node']['link']
                    for f in fw_node_link_list:
                        if f['rel'] == 'status':
                            fw_node_status_ref = str(f['href']).replace(self._smc_ref, '')
                            break
                    result = smc_connection.get(fw_node_status_ref)
                    status = result[0]['status']
                    if status != wait_for_status:
                        LOG.debug("Firewall status {0}".format(status))
                        yield cfg.CONF.NGFW.fw_status_polling_interval
                    else:
                        smc_connection.logout()
                        break
                except:
                    LOG.error("Failed to get fw status {0}".format(router_ref))
                    smc_connection.logout()
                    raise

        try:
            self._wait(_fw_status, cfg.CONF.NGFW.fw_status_polling_timeout, router_ref, 'No Policy Installed')
        except:
            LOG.error("Failed to wait for fw status {0}".format(router_ref))
            self._novaclient.servers.delete(ngfw)
            self._core_plugin.delete_port(context.elevated(), mgmt_port['id'])
            smc_connection.login()
            smc_connection.delete(router_ref)
            smc_connection.logout()
            raise

        # Create an empty policy and upload to ngfw
        smc_connection.login()
        r = smc_connection.get('elements/fw_template_policy')
        fw_template_list = r[0]['result']
        for tplt in fw_template_list :
            if tplt['name'] == "Firewall Template":
                fw_template_ref = tplt['href'].replace(self._smc_ref, '')

        if not fw_template_ref:
            LOG.error("Failed to find Firewall Template")
            raise exceptions.NotFound

        policy_name = self._ngfw_policy_name(router_id)
        fw_policy = {
                     "name" : policy_name,
                     "template" : fw_template_ref
        }

        json_data = json.dumps(fw_policy)

        r = smc_connection.post_element('fw_policy', json_data)
        policy_ref = r.headers['location']
        policy_ref = str(policy_ref).replace(self._smc_ref, '')

        r = smc_connection.session.post(self._smc_ref + router_ref + "/upload?filter={0}".format(policy_name))
        self._pp.pprint(r)
        smc_connection.logout()

        # Wait firewall status to turn to "Online"
        try:
            self._wait(_fw_status, cfg.CONF.NGFW.fw_status_polling_timeout, router_ref, 'Online')
        except:
            LOG.error("Failed to wait for fw status {0}".format(router_ref))
            self._novaclient.servers.delete(ngfw)
            self._core_plugin.delete_port(context.elevated(), mgmt_port['id'])
            smc_connection.login()
            smc_connection.delete(router_ref)
            smc_connection.delete(policy_ref)
            smc_connection.logout()
            raise

        return mgmt_port['id'] # TODO: random return value

    def _wait(self, poll_fn, timeout=0, *poll_fn_args):
            now = time.time()
            for interval in poll_fn(*poll_fn_args):
                greenthread.sleep(interval)
                if timeout > 0 and (time.time() - now) > timeout:
                    raise TimeoutException()

    def delete_router(self, context, router_id):
        ngfw_name = 'ngfw_' + router_id
        
        router_ref = self._get_ngfw_ref(ngfw_name)
        
        # TODO: also has to remove the policies and rules from SMC
        self._smc_connection.login()
        self._smc_connection.delete(router_ref)
        policy = self._get_ngfw_policy_ref(ngfw_name)
        self._smc_connection.delete(policy)
        self._smc_connection.logout()
        
        self._delete_vm_by_name(ngfw_name)

    ''' TODO: this function logs out the smc connection session '''
    def _get_ngfw_ref(self, router_name):
        smc_connection = self._smc_connection
        smc_connection.login()
        router_ref = None
        try:
            result = smc_connection.get("elements/single_fw")
        except:
            smc_connection.logout()
            raise
        
        firewall_list = result[0]['result']
        for fw in firewall_list:
            if fw['name'] == router_name:
                router_ref = str(fw['href']).replace(self._smc_ref, '')
                print "XXXXXXXXX"
                print "router_ref", router_ref
                break
        if router_ref == None:
            LOG.error("failed to lookup router {0} in SMC".format(router_name))
            raise NoRouterException

        smc_connection.logout()
        return router_ref

    def _get_ngfw_policy_ref(self, policy_name):
        smc_connection = self._smc_connection
        smc_connection.login()

        try:
            result = smc_connection.get("elements/fw_policy?filter={0}".format(policy_name))
        except:
            LOG.error("Failed to get fw policy {0}".format(policy_name))
            raise
        
        policy_ref = result[0]['result'][0]['href']
        policy_ref = str(policy_ref).replace(self._smc_ref, '')
        
        return policy_ref

    def _add_ngfw_interface(self, router_id, interface_id, ip, cidr):
        ngfw_name = self._ngfw_name(router_id)
        ngfw_ref = self._get_ngfw_ref(ngfw_name)
        smc_connection = self._smc_connection
        smc_connection.login()
        r = smc_connection.get(ngfw_ref, etag=True)
        data = r[0]
        etag = r[1]
        physical_interfaces = data['physicalInterfaces']

        physical_interface_template = """
{
      "physical_interface": {
        "aggregate_mode": "none",
        "arp_entry": [],
        "cvi_mode": "none",
        "dhcp_server_on_interface": {
          "default_lease_time": 7200,
          "dhcp_range_per_node": []
        },
        "interface_id": "@PLACE_HODLER@",
        "interfaces": [
          {
            "single_node_interface": {
              "address": "@PLACE_HOLDER_IP@",
              "auth_request": false,
              "auth_request_source": false,
              "automatic_default_route": false,
              "backup_heartbeat": false,
              "backup_mgt": false,
              "dynamic": false,
              "igmp_mode": "none",
              "network_value": "@PLACE_HOLDER_IP_NETWORK@",
              "nicid": "@PLACE_HOLDER_NICID@",
              "nodeid": 1,
              "outgoing": false,
              "pppoa": false,
              "pppoe": false,
              "primary_heartbeat": false,
              "primary_mgt": false,
              "relayed_by_dhcp": false,
              "reverse_connection": false,
              "vrrp": false,
              "vrrp_id": -1,
              "vrrp_priority": -1
            }
          }
        ],
        "log_moderation": [
          {
            "burst": 1000,
            "log_event": "1",
            "rate": 100
          },
          {
            "log_event": "2"
          }
        ],
        "managed_address_flag": false,
        "mtu": -1,
        "other_configuration_flag": false,
        "qos_limit": -1,
        "qos_mode": "no_qos",
        "router_advertisement": false,
        "syn_mode": "default",
        "virtual_engine_vlan_ok": false,
        "vlanInterfaces": []
      }
    }
"""
        json_data = json.loads(physical_interface_template)
        phys_iface = json_data['physical_interface']
        phys_iface['interface_id'] = str(interface_id)
        iface = json_data['physical_interface']['interfaces'][0]
        iface = iface['single_node_interface']
        iface['nicid'] = str(interface_id)
        iface['address'] = ip
        iface['network_value'] = cidr
        physical_interfaces.append(json_data)

        LOG.debug("putting data")
        self._pp.pprint(data)

        data = json.dumps(data)

        
        r = smc_connection.put(ngfw_ref, data, etag=etag)
        if r.code != 204:
            LOG.error("Failed to configure engine: %s" % (r.result))

        smc_connection.logout()

    def _remove_ngfw_interface(self, router_id, interface_id):
        ngfw_name = self._ngfw_name(router_id)
        ngfw_ref = self._get_ngfw_ref(ngfw_name)
        smc_connection = self._smc_connection

        smc_connection.login()

        r = smc_connection.get(ngfw_ref, etag=True)
        data = r[0]
        etag = r[1]

        # Remove the correspongind routing entries
        # Must be removed before removing the interface, otherwise the nic_id key is not present
        # in the routing_node
        r = None
        for link in data["link"]:
            if link["rel"] == "routing":
                routing_id = link["href"].split("/")[-1]
                r = smc_connection.get(
                    "{}/routing/{}".format(ngfw_ref, routing_id),
                    etag=True) # TODO: etag=True?
                routing_data = r[0]
                break

        if not routing_data:
            LOG.error("BUG: No routing data found for interface %s" %
                      (interface_id))
            return

        for node in routing_data['routing_node']:
            if int(node["nic_id"]) == int(interface_id):
                smc_connection.delete(ngfw_ref + "/routing/{}".format(
                    node["link"][0]["href"].split("/")[-1]))
                break

        physical_interfaces = data['physicalInterfaces']
        for phy_ifce in physical_interfaces:
            ifce_id = phy_ifce['physical_interface']['interface_id']
            if int(ifce_id) == int(interface_id):
                physical_interfaces.remove(phy_ifce)
                break
        
        r = smc_connection.put(ngfw_ref, json.dumps(data), etag=etag)

        smc_connection.logout()

    def add_router_interface(self, context, router_id, dict_info, interface_id):
        return self._add_router_interface(context, router_id, dict_info['port_id'], interface_id)

    def _add_router_interface(self, context, router_id, router_port_id, interface_id):
        '''TODO: caller of these functions seem to be duplicating code.
        '''
        port = self._core_plugin._get_port(context.elevated(), router_port_id)
        print "XXXXXXXXXXX add_router_interace() print port"
        print port
        "<neutron.db.models_v2.Port[object at 7faf5bb03350] {tenant_id=u'de37d87e3f214b87a2290f04bf0ce17e', id=u'b7f417c7-2617-4a56-9e77-881eac5b9c54', name=u'', network_id=u'676482a1-6ccc-4702-94b9-a90c9ed3c0e4', mac_address=u'fa:16:3e:ab:24:ad', admin_state_up=True, status=u'DOWN', device_id=u'1234', device_owner=u'network:router_interface'}>"
        print port.fixed_ips
        "[<neutron.db.models_v2.IPAllocation[object at 7f757a821710] {port_id=u'65b15ad8-5e04-441f-adb9-9f69f2f483b7', ip_address=u'192.168.1.1', subnet_id=u'bf2b05a0-679a-4b91-a82e-863ad9bf53b4', network_id=u'3a63e828-4440-4753-95e0-283d002a3233'}>]"
        
        router_port_ip = port.fixed_ips[0]['ip_address']
        #subnet = self._core_plugin._get_subnet(context, dict_info['subnet_id'])
        subnet = self._core_plugin._get_subnet(context, port.fixed_ips[0]['subnet_id'])
        router_port_cidr = subnet['cidr']
        print "XXXXXXXXX print subnet"
        print subnet
        "<neutron.db.models_v2.Subnet[object at 7f4e2d9fd7d0] {tenant_id=u'de37d87e3f214b87a2290f04bf0ce17e', id=u'bf2b05a0-679a-4b91-a82e-863ad9bf53b4', name=u'test subnet', network_id=u'3a63e828-4440-4753-95e0-283d002a3233', ip_version=4L, cidr=u'192.168.1.0/24', gateway_ip=u'192.168.1.1', enable_dhcp=True, shared=False, ipv6_ra_mode=None, ipv6_address_mode=None}>"

        
        ngfw_name = self._ngfw_name(router_id)
        policy_name = self._ngfw_policy_name(router_id)
        mac_address = self._generate_mac_address(router_id, interface_id)

        try:
            new_port = self._core_plugin.create_port(context.elevated(), {
                                'port': {'tenant_id': cfg.CONF.NGFW.tenant_id,
                                         'network_id': subnet['network_id'],
                                         'mac_address': mac_address,
                                         'fixed_ips': attributes.ATTR_NOT_SPECIFIED,
                                         'device_owner': '',
                                         'device_id': '',
                                         'admin_state_up': True,
                                         'name': ''}})
        except:
            LOG.error("Failed to create port on network {0}".format(subnet['network_id']))
            raise

        new_port_id = new_port['id']

        try:
            ngfw_vm = self._get_vm_by_name(ngfw_name)
            ngfw_vm.interface_attach(new_port['id'], None, None)
        except:
            LOG.error("Failed to attach port to ngfw VM {0}".format(ngfw_name))
            self._core_plugin.delete_port(context.elevated(), new_port['id'])
            raise

        try:
            #self._ngfw_add_new_ip(ngfw_name, gw_ip, subnet['cidr'])
            self._add_ngfw_interface(router_id,
                                     interface_id,
                                     router_port_ip,
                                     router_port_cidr)

            ngfw_network_ref = self._create_ngfw_network(ngfw_name, subnet['cidr'])
        
            policy_ref = self._get_ngfw_policy_ref(policy_name)

            rule_allow_to_any = {
                  "name" : subnet['cidr'] + '-allow_to_any',
                  "comment" : subnet['cidr'],
                  "action":
                          {
                                "action": 'allow',
                                "connection_tracking_options":
                                    {
                                    }
                           },
                          "destinations": { 'any' : True },
                          "services": { 'any' : True},
                          "sources": { "src" : [ ngfw_network_ref ] }
                          }

            smc_connection = self._smc_connection
            smc_connection.login()
        
            json_data = json.dumps(rule_allow_to_any)
            LOG.debug("Inserting rule rule_allow_to_any")
            r = smc_connection.post(policy_ref + "/fw_ipv4_access_rule", json_data)
            print r
            rule_allow_from_any = {
                               "name" : subnet['cidr'] + '-allow_from_any',
                               "comment" : subnet['cidr'],
                               "action" : {
                                           "action": 'allow',
                                           "connection_tracking_options":
                                                                        {
                                                                        }
                                           },
                               "destinations": { 'dst' : [ ngfw_network_ref ] },
                               "services": { 'any' : True},
                               "sources": { 'any' : True }
                               }

            json_data = json.dumps(rule_allow_from_any)
            LOG.debug("Inserting rule rule_allow_from any")
            r = smc_connection.post(policy_ref + "/fw_ipv4_access_rule", json_data)
            print r        

        except:
            LOG.error("Failed to set up router rules")
            self._core_plugin.delete_port(context.elevated(), new_port['id'])
            raise

        return new_port_id

    def _ngfw_name(self, router_id):
        return 'ngfw_' + router_id

    def _ngfw_policy_name(self, router_id):
        return self._ngfw_name(router_id) + '-policy'

    def remove_router_interface(self, context, router_id, router_port,
                                ngfw_port_id, interface_id):

        # TODO: wrapper for name generation based on router_id
        ngfw_name = self._ngfw_name(router_id)
        policy_name = self._ngfw_name(router_id)

        subnet_id = router_port['fixed_ips'][0]['subnet_id']
        router_port_ip = router_port['fixed_ips'][0]['ip_address']

        subnet = self._core_plugin._get_subnet(context, subnet_id)
        
        policy_ref = self._get_ngfw_policy_ref(policy_name)
        
        smc_connection = self._smc_connection
        smc_connection.login()
        r = smc_connection.get(policy_ref + "/fw_ipv4_access_rule")
        r = r[0]['result']
        
        for l in r:
            rule_ref = str(l['href']).replace(self._smc_ref, '')
            rule = smc_connection.get(rule_ref)
            comment = rule[0]['comment']
            if comment == subnet['cidr']:
                smc_connection.delete(rule_ref)

        networks = smc_connection.get('elements/network')[0]['result']
        for net in networks:
            if net['name'] == "network-%s-%s" % (ngfw_name, subnet['cidr']):
                smc_connection.delete(str(net['href']).replace(self._smc_ref, ''))

        if interface_id:
            self._ngfw_delete_ip(ngfw_name, router_port_ip)
            self._remove_ngfw_interface(router_id, interface_id)

        if ngfw_port_id:
            self.ngfw_delete_port(context, router_id, ngfw_port_id)

        # TODO: who removes gateway related config from SMC?

    def ngfw_delete_port(self, context, router_id, ngfw_port_id):
        '''Delete NGFW port create by this plugin
        TODO: currently ngfw hot unplug is unpredictable
        '''
        ngfw_vm = self._get_vm_by_name(self._ngfw_name(router_id))
        ngfw_vm.interface_detach(ngfw_port_id)
        self._core_plugin.delete_port(context, ngfw_port_id, l3_port_check=False)

    def refresh_ngfw_policy(self, router_id):
        '''TODO: refresh new policy before hotunplugging a port.
        '''
        ngfw_ref = self._get_ngfw_ref(self._ngfw_name(router_id))

        self._smc_connection.login()
        r = self._smc_connection.session.post(self._smc_ref + ngfw_ref + "/refresh")
        self._smc_connection.logout()

    def _add_gateway_info(self, context, router_id, gw_port_id, nic_id):
        '''
        - Add the IP of the gw_port_id interface as the default for outgoing
        - Add the subnet gateway IP of gw_port as the default gateway for the engine
        - Configure default NAT for the engine
        '''
        ngfw_name = 'ngfw_' + router_id
        gw_port = self._core_plugin._get_port(context.elevated(), gw_port_id)
        ngfw_ip = gw_port.fixed_ips[0]['ip_address']
        subnet_id = gw_port.fixed_ips[0]['subnet_id']
        subnet = self._core_plugin._get_subnet(context, subnet_id)
        default_gw_ip = subnet['gateway_ip']
        # cidr in this format '192.168.1.0/24'
        cidr = subnet['cidr']
        
        ngfw_ref = self._get_ngfw_ref(ngfw_name)

        smc_connection = self._smc_connection

        smc_connection.login()

        r = smc_connection.get(ngfw_ref, etag=True)
        engine_element = r[0]

        etag = r[1]
        # Enable default NAT
        engine_element["default_nat"] = True
        
        # Set the gw facing nic as the default for outgoing
        physical_interfaces = engine_element['physicalInterfaces']

        for phy_iface in physical_interfaces:
            for interface in phy_iface['physical_interface']['interfaces']:
                iface = interface['single_node_interface']
                if int(iface["nicid"]) == int(nic_id):
                    iface["outgoing"] = True
                else:
                    iface["outgoing"] = False
        
        # Add router element for GW and set it as default router
        #POST: http://192.168.206.245:8082/5.8/elements/single_fw/174/add_route?gateway=2.2.2.254&network=0.0.0.0/0
        r = smc_connection.post(
            ngfw_ref + "/add_route?gateway={}&network=0.0.0.0/0".format(default_gw_ip), None)

        print(engine_element)
        data = json.dumps(engine_element)
        r = smc_connection.put(ngfw_ref, data, etag=etag)
        print("Add interface put: " + str(r))
        smc_connection.logout()

    def _delete_gateway_info(self, context, router_id, gw_port_id):
        '''  '''
        gw_port = self._core_plugin._get_port(context.elevated(), gw_port_id)
        gw_ip = gw_port.fixed_ips[0]['ip_address']
        subnet_id = gw_port.fixed_ips[0]['subnet_id']
        subnet = self._core_plugin._get_subnet(context, subnet_id)
        # cidr in this format '192.168.1.0/24'
        cidr = subnet['cidr']
        
        smc_connection = self._smc_connection
        pass

    def _create_ngfw_network(self, ngfw_name, cidr):
        net_json_def = {
                        #currently we do not support adding multiple interfaces to one subnet
                        "name" : "network-%s-%s" % (ngfw_name, str(cidr)),
                        "ipv4_network" : cidr
                       }

        json_data = json.dumps(net_json_def)
        smc_connection = self._smc_connection
        smc_connection.login()

        # public and internal network are pre-created in smp_api.createL3FW() if corresponding cidrs are passed in
        r = smc_connection.get("elements/network")
        networks = r[0]['result']
        for net in networks:
            if net['name'] == "network-%s-%s" % (ngfw_name, cidr):
                ref = net['href']
                smc_connection.logout()
                return ref

        r = smc_connection.post_element("network", json_data)
        smc_connection.logout()
        ref = r.headers['location']
        return ref

    def _get_vm_by_name(self, vm_name):
        servers = self._novaclient.servers.list()
        for server in servers:
            if server.name == vm_name:
                return server
        return None

    def _delete_vm_by_name(self, vm_name):
        vm = self._get_vm_by_name(vm_name)
        if vm == None:
            LOG.error("Failed to find VM with name {0}".format(vm_name))
            return
        self._novaclient.servers.delete(vm)

    def _ngfw_add_new_ip(self, ngfw_name, new_ip, cidr):
        
        ngfw_ref = self._get_ngfw_ref(ngfw_name)
        smc_connection = self._smc_connection
        smc_connection.login()
        r = smc_connection.get(ngfw_ref, etag=True)
        
        etag = r[1]
        data = r[0]
        self._pp.pprint(data)

        single_node_interface_template = {
            "single_node_interface": {
              "address": new_ip,
              "auth_request": False,
              "auth_request_source": False,
              "backup_heartbeat": False,
              "backup_mgt": False,
              "dynamic": False,
              "igmp_mode": "none",
              "network_value": cidr,
              "nicid": "1",
              "nodeid": 1,
              "outgoing": False,
              "pppoa": False,
              "pppoe": False,
              "primary_heartbeat": False,
              "primary_mgt": False,
              "relayed_by_dhcp": False,
              "reverse_connection": False,
              "vrrp": False,
              "vrrp_id": -1,
              "vrrp_priority": -1
            }
        }

        itfce = None
        for phy_itfce in data["physicalInterfaces"]:
            if phy_itfce["physical_interface"]["interfaces"][0]["single_node_interface"]["address"] == "0.0.0.0":
                itfce = phy_itfce["physical_interface"]["interfaces"][0]["single_node_interface"]
                single_node_interface_template["single_node_interface"]["nicid"] = itfce["nicid"]
                single_node_interface_template["single_node_interface"]["nodeid"] = itfce["nodeid"]
                phy_itfce["physical_interface"]["interfaces"].append(single_node_interface_template)

        if itfce is None:
            LOG.error("Failed to look up NGFW outgoing interface")
            raise exceptions.Invalid
        
        #data["physicalInterfaces"][0]["physical_interface"]["interfaces"].append(single_node_interface_template)
        print "XXXXXXXXXXXXXXXXx"
        print
        print
        self._pp.pprint(data)

        data = json.dumps(data)
        r = smc_connection.put(ngfw_ref, data, etag=etag)
        smc_connection.logout()
        
    def _ngfw_delete_ip(self, ngfw_name, delete_ip):
        
        ngfw_ref = self._get_ngfw_ref(ngfw_name)
        smc_connection = self._smc_connection
        smc_connection.login()
        r = smc_connection.get(ngfw_ref, etag=True)
        
        etag = r[1]
        data = r[0]
        self._pp.pprint(data)
 
        
        found = False
        for phy_itfce in data["physicalInterfaces"]:
            index = 0
            # TODO: make a generic iterator routing for this loop
            # so that it handles the case of iface with no IPs configured
            for itfce in phy_itfce["physical_interface"]["interfaces"]:
                print "interface address = %s delete_ip = %s" % (itfce['single_node_interface']['address'], delete_ip)
                if itfce['single_node_interface']['address'] == delete_ip:
                    phy_itfce["physical_interface"]["interfaces"].pop(index)
                    found = True
                    break
                index += 1
                
        print "XXXXXXXXXXXXXXXXx"
        print
        print
        
        if not found:
            LOG.error("Can not find the ip address in SMC")
            # do not throw out exceptions to avoid affecting
            # the following operations
            smc_connection.logout()
            return
        
        self._pp.pprint(data)

        data = json.dumps(data)
        r = smc_connection.put(ngfw_ref, data, etag=etag)
        smc_connection.logout()

    def insert_dynamic_NAT_rule(self, router_id, internal_cidr, external_ip):
        pass

    def create_floatingip(self, router_id, internal_ip, external_ip, external_cidr):
        '''
        '''

        # Create a host element for the internal host
        '''
        {
        "address": "1.2.3.4",
        "name": "xtest"
        }
        '''
        internal_host = self.ngfw_create_host(
            self._floatingip_hostname(internal_ip), internal_ip)

        # Add a new NAT definition for the engine element:

        ngfw_ref = self._get_ngfw_ref(self._ngfw_name(router_id))
        smc_connection = self._smc_connection
        smc_connection.login()
        r = smc_connection.get(ngfw_ref, etag=True)
        data = r[0]
        etag = r[1]
        nat_definitions = data['nat_definition']

        nat_definition_template = '''
    {
      "enabled_interface": [],
      "nat_type": "static",
      "private_ne_ref": "",
      "public_ip": "",
      "service_ref": []
    }        
        '''
        #      "private_ne_ref": "http://192.168.206.245:8082/5.8/elements/host/229",

        new_definition = json.loads(nat_definition_template)
        new_definition["private_ne_ref"] = internal_host
        new_definition["public_ip"] = external_ip

        nat_definitions.append(new_definition)

        r = smc_connection.put(ngfw_ref, json.dumps(data), etag=etag)
        # TODO: are these codes right?
        if r.code != 200:
            LOG.error("Failed to configure engine: %s" % (r.result))

        smc_connection.logout()

    
    def _floatingip_hostname(self, host_ip):
        return "floatingip-host-%s" % str(host_ip)

    def delete_floatingip(self, router_id, external_ip, internal_ip):

        ''' router_id is None means the floatingip is not associated
        with any router '''
        # TODO: the host element is never removed
        if not router_id:
            #TODO: smart?
            # TODO: still remove the host element
            return

        ngfw_ref = self._get_ngfw_ref(self._ngfw_name(router_id))
        smc_connection = self._smc_connection
        smc_connection.login()
        r = smc_connection.get(ngfw_ref, etag=True)
        data = r[0]
        etag = r[1]
        nat_definitions = data['nat_definition']
        host_ref = None

        for d in nat_definitions:
            if d["public_ip"] == external_ip:
                host_ref = d["private_ne_ref"]
                nat_definitions.remove(d)
                break

        r = smc_connection.put(ngfw_ref, json.dumps(data), etag=etag)
        # TODO: are these codes right?
        if r.code != 200:
            LOG.error("Failed to configure engine: %s" % (r.result))

        # Remove the host element for the public IP
        smc_connection.delete(host_ref)
        smc_connection.logout()

        #self._remove_host(self._floatingip_hostname(internal_ip))

    def _get_host_element(self, host_name, host_ip):
        self._smc_connection.login()
        try:
            result = self._smc_connection.get("elements/host")
        except:
            # TODO: uniform error handling for this
            self._smc_connection.logout()
            raise
        
        for host in result[0]["result"]:
            if host["name"] == host_name:
                # TODO: get the href and compare the IPs
                return host["href"]
                '''
                if host["address"] == host_ip:
                    return host["href"]
                else:
                    raise("Host name already in use with other IP")
                '''
        return None

    def ngfw_create_host(self, host_name, host_ip):
        host = self._get_host_element(host_name, host_ip)
        if not host:
            self._ngfw_create_host(self, host_name, host_ip)
        else:
            return host

    def _ngfw_create_host(self, host_name, host_ip):
        # TODO: fails if name exists. Return that instead?
        host_json_def = {
                       "name": host_name,
                       "address": host_ip
                       }

        json_data = json.dumps(host_json_def)

        smc_connection = self._smc_connection
        smc_connection.login()
        r = smc_connection.post_element("host", json_data)
        smc_connection.logout()
        # TODO:...
        if r.code == 422:
            raise("create host failed")
        ref = r.headers['location']
        
        return ref

    def _ngfw_delete_host(self, host_name):
        # TODO: use get_host_element
        smc_connection = self._smc_connection
        smc_connection.login()
        router_ref = None
        try:
            result = smc_connection.get("elements/host")
        except:
            smc_connection.logout()
            raise
        
        for host in result[0]["result"]:
            if host["name"] == host_name:
                smc_connection.delete(host["href"])
        
class VmStatusError(exceptions.NeutronException):
    def __init__(self, vm_type):
        """ vm_type is 'ngfw' or 'shim' """
        self._vm_type = vm_type

    def __str__(self):
        return "Failed to spawn {0} VM instance".format(self._vm_type)

class TimeoutException(exceptions.NeutronException):
    message = _("Waiting VM spawn timed out")

class NoRouterException(exceptions.NeutronException):
    message = _("Failed to get Router reference in SMC")
