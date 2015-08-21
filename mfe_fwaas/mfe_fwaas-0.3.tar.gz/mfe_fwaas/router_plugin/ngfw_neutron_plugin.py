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

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import exc

from oslo_config import cfg
from oslo_utils import importutils

from neutron.db import common_db_mixin
from neutron.db import extraroute_db
from neutron.db import l3_gwmode_db
from neutron.db import model_base
from neutron.db import models_v2
from neutron.api.rpc.agentnotifiers import l3_rpc_agent_api
from neutron.api.rpc.handlers import l3_rpc
from neutron.common import constants as q_const
from neutron.common import rpc as n_rpc
from neutron.common import topics
from neutron.db import l3_hascheduler_db
from neutron.db.l3_db import RouterPort
from neutron.db.l3_db import L3_NAT_db_mixin
from neutron.plugins.common import constants
from neutron.services.l3_router.mcafee import ngfw_driver
from oslo_log import log as logging
from neutron.db import l3_db
from neutron.extensions import l3
from neutron.common import constants as l3_constants


import pprint
import copy
import pdb

LOG = logging.getLogger(__name__)

# TODO: how do we know if the vm is scheduled in L3 node, do we care?
# TODO: per tenant isolation in db?
# The next available interface ID,
# get and increase in an atomic operation
class MfeInterfaceIdMap(model_base.BASEV2):
    router_id = sa.Column(
        sa.String(36),
        sa.ForeignKey('routers.id'),
        primary_key=True)

    interface_id = sa.Column(sa.Integer)

# One router port has two corresponding ports in shim vm.
# When shim vm is removed, this DB should represent the mapping of
# router port to the corresponding port inserted to ngfw vm.
class MfeRouterPortMap(model_base.BASEV2):
    ngfw_port = sa.Column(
        sa.String(36),
        sa.ForeignKey('ports.id'),
        primary_key=True)

    router_port = sa.Column(sa.String(36))
    interface_id = sa.Column(sa.Integer)
    router_id = sa.Column(sa.String(36))

class NgfwL3RpcCallback(l3_rpc.L3RpcCallback):
    def sync_routers(self, context, **kwargs):
        '''L3 plugins will always get an empty list of routers.
        '''
        #pdb.set_trace()
        routers = super(NgfwL3RpcCallback, self).sync_routers(context, **kwargs)
        cleared_values = {"_interfaces": [], "gw_port": None, "external_gateway_info": {}}
        for r in routers:
            for key in cleared_values.keys():
                #del r[key]
                r[key] = cleared_values[key]
        return routers

class NgfwRouterPlugin(common_db_mixin.CommonDbMixin,
#                       extraroute_db.ExtraRoute_db_mixin,
                       extraroute_db.ExtraRoute_dbonly_mixin,
                       l3_gwmode_db.L3_NAT_dbonly_mixin,
#                       l3_gwmode_db.L3_NAT_db_mixin,
                       l3_hascheduler_db.L3_HA_scheduler_db_mixin):
    """
    McAfee Neutron L3 plugin for NGFW
    """

    supported_extension_aliases = ["router", "ext-gw-mode", "extraroute"]
#   supported_extension_aliases = ["router", "ext-gw-mode"]

    def __init__(self):
        super(NgfwRouterPlugin, self).__init__()
        
        self.setup_rpc()

        self.router_scheduler = importutils.import_object(
            cfg.CONF.router_scheduler_driver)

        self.driver = ngfw_driver.NgfwRouterDriver()

        self._pp=pprint.PrettyPrinter()

    def setup_rpc(self):
        # RPC support
        self.topic = topics.L3PLUGIN
        self.conn = n_rpc.create_connection(new=True)
        self.agent_notifiers.update(
            {q_const.AGENT_TYPE_L3: l3_rpc_agent_api.L3AgentNotifyAPI()})
        #self.endpoints = [l3_rpc.L3RpcCallback()]
        self.endpoints = [NgfwL3RpcCallback()]
        self.conn.create_consumer(self.topic, self.endpoints,
                                  fanout=False)
        self.conn.consume_in_threads()

    def get_plugin_type(self):
        return constants.L3_ROUTER_NAT

    def get_plugin_description(self):
        """Returns string description of the plugin"""
        return ("McAfee NGFW Router Service Plugin for basic L3 forwarding "
                "between neutron networks and external networks")

    def _generate_ngfw_interface_id(self, context, router_id):
        with context.session.begin(subtransactions=True):
            qry = context.session.query(MfeInterfaceIdMap)
            qry = qry.filter_by(router_id=router_id)
            ngfw_interface_id = qry.one()
            # this is multi-thread safe?
            interface_id = ngfw_interface_id.interface_id
            ngfw_interface_id.interface_id = ngfw_interface_id.interface_id + 1
        
        return interface_id

    def create_router(self, context, router):
        #pdb.set_trace()
        router_deep_copy = copy.deepcopy(router)
        router_dict = super(NgfwRouterPlugin, self).create_router(context, router)

        router_deep_copy['router']['id'] = router_dict['id']
        router_id = router_dict['id']
        
        try:        
            mgmt_port_id = self.driver.create_router(context, router_deep_copy)
            routerport2ngfwport = MfeRouterPortMap(router_port=0, # TODO!?
                                                      ngfw_port=mgmt_port_id,
                                                      interface_id=0,
                                                      router_id=router_id)
            context.session.add(routerport2ngfwport)

        except:
            LOG.error("Failed to create ngfw router, bailing out ...")
            super(NgfwRouterPlugin, self).delete_router(context, router_id)
            raise

        try:
            with context.session.begin(subtransactions=True):
                '''ID 0 is hardcoded to the mgmt interface '''
                interface_id = 1
                router_entry = MfeInterfaceIdMap(router_id=router_id,
                                               interface_id=interface_id)
                context.session.add(router_entry)                

        except:
            LOG.error("Failed to add ngfw information to interface DB")
            self.driver.delete_router(context, router_id)
            super(NgfwRouterPlugin, self).delete_router(context, router_id)
            raise

        if router_dict[l3.EXTERNAL_GW_INFO]:
            # TODO: duplicate code to update_router
            gw_port_id = router_dict['gw_port_id']
            interface_id = self._generate_ngfw_interface_id(context, router_id)
            try:    
                ngfw_port_id = self.driver._add_router_interface(context,
                                                                 router_id,
                                                                 gw_port_id,
                                                                 interface_id)
            except:
                LOG.error("Failed to create internal interface for gateway port")
                super(NgfwRouterPlugin, self).delete_router(context, router_id)
                raise
                               
            try:
                self.driver._add_gateway_info(context, router_id, gw_port_id,
                                              interface_id)

                with context.session.begin(subtransactions=True):
                    routerport2ngfwport = MfeRouterPortMap(router_port=gw_port_id,
                                                              ngfw_port=ngfw_port_id,
                                                              interface_id=interface_id,
                                                              router_id=router_id)
                    context.session.add(routerport2ngfwport)

            except:
                LOG.error("Failed to add gateway info to NGFW")
                '''
                self.driver.remove_router_interface(context, router_id,
                                                    gw_port,
                                                    ngfw_port,
                                                    interface_id)
                super(NgfwRouterPlugin, self).delete_router(context, router_id)
                '''
                raise            

        self.driver.refresh_ngfw_policy(router_id)
        print("SUCCESS: router created")
        return router_dict

    def update_router(self, context, router_id, router):
        '''

        TODO: external NIC is always removed causing new NIC id to be requested.
        NIC IDs will run out at some point.
        '''
        #pdb.set_trace()
        r = self._get_router(context, router_id)
        self._pp.pprint(r)
        
        if r['gw_port_id']:
            old_gw_port_id = r['gw_port_id']
            old_gw_port = self._core_plugin._get_port(context.elevated(), old_gw_port_id)
   
            qry = context.session.query(MfeRouterPortMap)
            qry = qry.filter_by(router_port=old_gw_port_id)

            ngfw_port_id = None
            interface_id = None
            routerport2ngfwport = None

            try:
                routerport2ngfwport = qry.one()
                ngfw_port_id = routerport2ngfwport['ngfw_port']
                interface_id = routerport2ngfwport['interface_id']

            except exc.NoResultFound:
                #raise l3.RouterInterfaceNotFound(router_id=router_id,
                #port_id=old_gw_port_id)
                LOG.error("BUG: No port mapping for %s" % (old_gw_port_id))

            try: 
                self.driver._delete_gateway_info(context, router_id, old_gw_port_id)            
                self.driver.remove_router_interface(context,
                                                    router_id,
                                                    old_gw_port,
                                                    ngfw_port_id,
                                                    interface_id)

                if routerport2ngfwport:
                    with context.session.begin(subtransactions=True):
                        context.session.delete(routerport2ngfwport)
            except:
                ''' Only logging here, need to continue even if there is an error.
                    Because no way to fall back.
                '''
                LOG.error("Failed to delete old gateway")
                raise # TODO: remove?

        dict_info = super(NgfwRouterPlugin, self).update_router(context, router_id, router)
        #self.notify_router_updated(context, router_info['id'], None)

        print "XXXXXXXXXX"
        self._pp.pprint(dict_info)

        if dict_info[l3.EXTERNAL_GW_INFO]:
            gw_port_id = dict_info['gw_port_id']
            interface_id = self._generate_ngfw_interface_id(context, router_id)
            try:
                ngfw_port_id = self.driver._add_router_interface(context,
                                                                 router_id,
                                                                 gw_port_id,
                                                                 interface_id)
                
                with context.session.begin(subtransactions=True):
                    routerport2ngfwport = MfeRouterPortMap(router_port=gw_port_id,
                                                              ngfw_port=ngfw_port_id,
                                                              interface_id=interface_id,
                                                              router_id=router_id)
                    context.session.add(routerport2ngfwport)
 
                self.driver._add_gateway_info(context, router_id, gw_port_id, interface_id)
            except:
                '''
                    Only logging here, need to continue even if there is an error.
                    Because no way to fall back.
                '''
                LOG.error("Failed to add new gateway")
                raise # TODO: remove?

        self.driver.refresh_ngfw_policy(router_id)
        return dict_info

    def delete_router(self, context, router_id):


        router = self._get_router(context, router_id)
        for rp in router.attached_ports.all():
            qry = context.session.query(MfeRouterPortMap)
            qry = qry.filter_by(router_port=rp.port.id)

            ngfw_port_id = None
            interface_id = None

            routerport2ngfwport = None
            try:
                routerport2ngfwport = qry.one()
                ngfw_port_id = routerport2ngfwport['ngfw_port']
                interface_id = routerport2ngfwport['interface_id']

            except exc.NoResultFound:
                LOG.error("BUG: no port mapping for %s" % (rp.port.id))

            try:
                self.driver.remove_router_interface(context,
                                                    router_id,
                                                    rp.port,
                                                    ngfw_port_id,
                                                    interface_id)
                if routerport2ngfwport:
                    with context.session.begin(subtransactions=True):
                        context.session.delete(routerport2ngfwport)
            except:
                '''
                    Only Logging here, we need to continue even if there is an error.
                    Because no way to fall back
                '''
                LOG.error("Failed to remove ngfw port")

        # Remove the mgmt interface.
        #pdb.set_trace()
        qry = context.session.query(MfeRouterPortMap)
        for port in qry.filter_by(router_id=router_id):
            self.driver.ngfw_delete_port(context, router_id, port['ngfw_port'])

        self.driver.delete_router(context, router_id)
        return super(NgfwRouterPlugin, self).delete_router(context, router_id)
        # TODO: remove MfeInterfaceIdMap table entry

    def add_router_interface(self, context, router_id, interface_info):
        self._pp.pprint(interface_info)
        "{u'subnet_id': u'bf2b05a0-679a-4b91-a82e-863ad9bf53b4'}"
        # if it is subnet, l3_db.add_router_interface will create the port on behalf of us
        #dict_info = super(NgfwRouterPlugin, self).add_router_interface(context, router_id, interface_info)

        dict_info = super(l3_gwmode_db.L3_NAT_dbonly_mixin, self).add_router_interface(
            context, router_id, interface_info)

        print "XXXXXXXXXXXX add_router_interface() print dict_info"
        print dict_info
        "{'subnet_id': u'bf2b05a0-679a-4b91-a82e-863ad9bf53b4', 'tenant_id': u'de37d87e3f214b87a2290f04bf0ce17e', 'port_id': '1b7c11af-e3c9-4159-a649-ecf0248b80f3', 'id': u'1234'}"

        interface_id = self._generate_ngfw_interface_id(context, router_id)

        try:
            ngfw_port_id = self.driver.add_router_interface(context,
                                                            router_id,
                                                            dict_info,
                                                            interface_id)
        except:
            super(NgfwRouterPlugin, self).remove_router_interface(context,
                                                                  router_id,
                                                                  interface_info)
            raise
        
        with context.session.begin(subtransactions=True):
            routerport2ngfwport = MfeRouterPortMap(
                router_port=dict_info['port_id'],
                ngfw_port=ngfw_port_id,
                interface_id=interface_id,
                router_id=router_id)
            context.session.add(routerport2ngfwport)

        self.driver.refresh_ngfw_policy(router_id)
        return dict_info

    def remove_router_interface(self, context, router_id, interface_info):
        #return super(NgfwRouterPlugin, self).remove_router_interface(context, router_id, interface_info)
        
        # remove by port or by subnet?
        router_port_id = interface_info.get('port_id')
        subnet_id = interface_info.get('subnet_id')
        device_owner = self._get_device_owner(context, router_id)
        
        if subnet_id:

            subnet = self._core_plugin._get_subnet(context, subnet_id)

            try:
                rport_qry = context.session.query(models_v2.Port).join(MfeRouterPortMap)
                ports = rport_qry.filter(
                                         RouterPort.router_id == router_id,
                                         RouterPort.port_type == device_owner,
                                         models_v2.Port.network_id == subnet['network_id']
                                         )

                for p in ports:
                    if p['fixed_ips'][0]['subnet_id'] == subnet_id:
                        router_port_id = p['id']
                        break

            except exc.NoResultFound:
                raise l3.RouterInterfaceNotFoundForSubnet(router_id=router_id,
                                                  subnet_id=subnet_id)

        qry = context.session.query(MfeRouterPortMap)
        qry = qry.filter_by(
            router_port=router_port_id
        )
        try:
            routerport2ngfwport = qry.one()
        except exc.NoResultFound:
            raise l3.RouterInterfaceNotFound(router_id=router_id,
                                             port_id=router_port_id)

        ngfw_port_id = routerport2ngfwport['ngfw_port']
        interface_id = routerport2ngfwport['interface_id']        
        router_port = self._core_plugin._get_port(context.elevated(), router_port_id)
        try:
            self.driver.remove_router_interface(context,
                                                router_id,
                                                router_port,
                                                ngfw_port_id,
                                                interface_id)
            with context.session.begin(subtransactions=True):
                context.session.delete(routerport2ngfwport)
        except:
            ''' Only Logging here, we need to continue even if there is an error.
                Because no way to fall back
            '''
            LOG.error("Failed to remove ngfw port")

        dict_info = super(NgfwRouterPlugin, self).remove_router_interface(context, router_id, interface_info)
        return dict_info

    def create_floatingip(self, context, floatingip):
        fip_dict =  super(NgfwRouterPlugin, self).create_floatingip(context, floatingip)
        '''
{'floating_network_id': u'cc1e598d-0936-4f5a-94d1-35d99cc64edf', 'router_id': None, 'fixed_ip_address': None, 'floating_ip_address': u'2.2.2.130', 'tenant_id': u'5c7439ab984145408cd2619dc518a6fb', 'status': 'ACTIVE', 'port_id': None, 'id': '0b120d2e-8bca-477b-8a38-de90a79716fb'}
        '''
        if fip_dict['fixed_ip_address'] is None:
            '''
                no association
            '''
            return fip_dict
        
        floating_network_id = fip_dict['floating_network_id']
        floating_subnet = self._core_plugin._get_subnets_by_network(context,
                                                                floating_network_id)[0]
        external_cidr = floating_subnet['cidr']
        external_ip = fip_dict['floating_ip_address']
        internal_ip = fip_dict['fixed_ip_address']
        router_id = fip_dict['router_id']

        self.driver.create_floatingip(router_id, internal_ip, external_ip, external_cidr)
        self.driver.refresh_ngfw_policy(router_id)
        
        return fip_dict

    def update_floatingip(self, context, floatingip_id, floatingip):
        fip = floatingip['floatingip']
        #return super(NgfwRouterPlugin, self).update_floatingip(context, floatingip_id, floatingip)

        fip_db = self._get_floatingip(context, floatingip_id)
        router_id = fip_db['router_id']
        external_ip = fip_db['floating_ip_address']
        internal_ip = fip_db['fixed_ip_address']
        self.driver.delete_floatingip(router_id, external_ip, internal_ip)
       
        fip_dict = super(NgfwRouterPlugin, self).update_floatingip(context, floatingip_id, floatingip)
        
        if fip['port_id'] is None:
            ''' port_id is None means disassociation '''
            return fip_dict
        
        floating_network_id = fip_dict['floating_network_id']
        floating_subnet = self._core_plugin._get_subnets_by_network(context,
                                                                floating_network_id)[0]
        external_cidr = floating_subnet['cidr']
        external_ip = fip_dict['floating_ip_address']
        internal_ip = fip_dict['fixed_ip_address']
        router_id = fip_dict['router_id']
        self.driver.create_floatingip(router_id, internal_ip, external_ip, external_cidr)
        
        # TODO: push policy?
        return fip_dict

    def delete_floatingip(self, context, floatingip_id):
        floatingip = self._get_floatingip(context, floatingip_id)
        router_id = floatingip['router_id']
        external_ip = floatingip['floating_ip_address']
        internal_ip = floatingip['fixed_ip_address']

        self.driver.delete_floatingip(router_id, external_ip, internal_ip)
        
        return super(NgfwRouterPlugin, self).delete_floatingip(context, router_id)

    # this interface is called from ML2 delete_port()  
    def disassociate_floatingips(self, context, port_id, do_notify=True):
        '''TODO: call super first and use the return router_ids
        '''
        with context.session.begin(subtransactions=True):
            fip_qry = context.session.query(l3_db.FloatingIP)
            floating_ips = fip_qry.filter_by(fixed_port_id=port_id)
            for floating_ip in floating_ips:
                router_id = floating_ip['router_id']
                external_ip = floating_ip['floating_ip_address']
                internal_ip = floating_ip['fixed_ip_address']
                if router_id:
                    ''' router_id is None means the floatingip is not associated with any router '''
                    self.driver.delete_floatingip(router_id, external_ip, internal_ip)

        return super(NgfwRouterPlugin, self).disassociate_floatingips(context, port_id)

        '''
        TODO: do we need to notify
        if do_notify:
            self.notify_routers_updated(context, router_ids)
            # since caller assumes that we handled notifications on its
            # behalf, return nothing
            return

        '''

    '''
    Override certain notification methods
    '''
    def notify_router_updated(self, context, router_id,
                              operation=None):
        pass
    '''
    def notify_routers_updated(self, context, router_ids,
                               operation=None, data=None):
        pass
    '''


    def notify_router_deleted(self, context, router_id):
        pass

    '''
    def update_router(self, context, id, router):
        router_dict = super(l3_gwmode_db.L3_NAT_db_mixin, self).update_router(context,
                                                                 id, router)
        #self.notify_router_updated(context, router_dict['id'], None)
        return router_dict
    '''
    '''
    def delete_router(self, context, id):
        super(l3_gwmode_db.L3_NAT_db_mixin, self).delete_router(context, id)
        #self.notify_router_deleted(context, id)
    '''

    def notify_router_interface_action(
            self, context, router_interface_info, action):
        l3_method = '%s_router_interface' % action
        #super(l3_gwmode_db.L3_NAT_dbonly_mixin, self).notify_routers_updated(
        #    context, [router_interface_info['id']], l3_method,
        #    {'subnet_id': router_interface_info['subnet_id']})

        mapping = {'add': 'create', 'remove': 'delete'}
        notifier = n_rpc.get_notifier('network')
        router_event = 'router.interface.%s' % mapping[action]
        #notifier.info(context, router_event,
        #              {'router_interface': router_interface_info})

    '''
    def add_router_interface(self, context, router_id, interface_info):
        router_interface_info = super(
            l3_gwmode_db.L3_NAT_db_mixin, self).add_router_interface(
                context, router_id, interface_info)
        #self.notify_router_interface_action(
        #    context, router_interface_info, 'add')
        return router_interface_info
    '''

    
    '''
    def remove_router_interface(self, context, router_id, interface_info):
        router_interface_info = super(
            l3_gwmode_db.L3_NAT_db_mixin, self).remove_router_interface(
                context, router_id, interface_info)
        #self.notify_router_interface_action(
        #    context, router_interface_info, 'remove')
        return router_interface_info
    '''

    '''
    def create_floatingip(self, context, floatingip,
            initial_status=l3_constants.FLOATINGIP_STATUS_ACTIVE):
        floatingip_dict = super(l3_gwmode_db.L3_NAT_db_mixin, self).create_floatingip(
            context, floatingip, initial_status)
        router_id = floatingip_dict['router_id']
        #self.notify_router_updated(context, router_id, 'create_floatingip')
        return floatingip_dict
    '''

    '''
    def update_floatingip(self, context, id, floatingip):
        old_floatingip, floatingip = self._update_floatingip(
            context, id, floatingip)
        router_ids = self._floatingips_to_router_ids(
            [old_floatingip, floatingip])
        #super(l3_gwmode_db.L3_NAT_db_mixin, self).notify_routers_updated(
        #    context, router_ids, 'update_floatingip', {})
        return floatingip
    '''

    '''
    def delete_floatingip(self, context, id):
        router_id = self._delete_floatingip(context, id)
        #self.notify_router_updated(context, router_id, 'delete_floatingip')
    '''

    '''
    def disassociate_floatingips(self, context, port_id, do_notify=True):
        """Disassociate all floating IPs linked to specific port.

        @param port_id: ID of the port to disassociate floating IPs.
        @param do_notify: whether we should notify routers right away.
        @return: set of router-ids that require notification updates
                 if do_notify is False, otherwise None.
        """
        router_ids = super(l3_gwmode_db.L3_NAT_db_mixin, self).disassociate_floatingips(
            context, port_id)
        if do_notify:
            #self.notify_routers_updated(context, router_ids)
            # since caller assumes that we handled notifications on its
            # behalf, return nothing
            return

        return router_ids
    '''

    def notify_routers_updated(self, context, router_ids):
        pass
        #super(l3_gwmode_db.L3_NAT_db_mixin, self).notify_routers_updated(
        #    context, list(router_ids), 'disassociate_floatingips', {})
