#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#          - Beraldo Leal <beraldo AT ncc DOT unesp DOT br>
#
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from odl.flow import ODLFlow
from odl.node import ODLNode
from odl.table import ODLTable
from odl.topology import ODLTopology

from odl.exceptions import *

from odl import log

import json
import sys
import requests


class ODLInstance(object):
    def __init__(self, server, credentials):
        self.server = server
        self.credentials = credentials
        self.headers = { 'Content-type' : 'application/json' }
        self.topology = ODLTopology(self.server, self.credentials, self)

    def to_dict(self):
        base = {'nodes': [ node.to_dict() for node in self.get_nodes().values() ]}

        # These links are from ODL topology plugin
        links = self.topology.get_links()
        result = []
        for link in links:
            source = link['source']['source-tp']
            target = link['destination']['dest-tp']
            result.append({'source': source, 'target': target})
        base['links'] = result

        connector_nodes = []
        # Now, creat our port-switch links
        for node in base['nodes']:
            id = node.keys()[0]
            connectors = node[id]['connectors']
            for connector in connectors:
                connector_id = connector.keys()[0]
                connector_nodes.append({connector_id: connector[connector_id]})
                port = connector[connector_id]['port_number']
                base['links'].append({'source': id, 'target': connector_id})

        # Extends nodes to include the connector_nodes
        base['nodes'].extend(connector_nodes)

        return base

    def request(self, method, endpoint, auth, data=None, content=None):
        if content:
            headers = {'Content-type': content}
        else:
            headers = self.headers

        if method == "GET":
            try:
                response = requests.get(endpoint,
                                        headers = headers,
                                        auth = auth)
            except requests.exceptions.RequestException as e:
                raise ODLErrorOnGET(e)
        elif method == "PUT":
            try:
                response = requests.put(endpoint,
                                        headers = headers,
                                        data = data,
                                        auth = auth)
            except requests.exceptions.RequestException as e:
                raise ODLErrorOnPUT(e)
        elif method == "DELETE":
            try:
                response = requests.delete(endpoint,
                                           headers = headers,
                                           auth = auth)
            except requests.exceptions.RequestException as e:
                raise ODLErrorOnDELETE(e)
        else:
            raise NotImplemented("Method %s not implemented." % method)

        if response.status_code == 404:
            raise ODL404("Endpoint not found: %s" % self.server + endpoint)

        # Consider any status other than 2xx an error
        if not response.status_code // 100 == 2:
            raise UnexpectedResponse(format(response))

        log.info("ODLInstance: %s %s" % (method, endpoint))
        return response

    def get(self, endpoint):
        """
        Requests a GET to endpoint and returns the json.
        """
        response = self.request(method = "GET",
                                endpoint = self.server + endpoint,
                                auth = self.credentials)
        return json.loads(response.text)

    def put(self, endpoint, data, content="application/json"):
        """
        Sends data via PUT to endpoint.
        """
        response = self.request(method = "PUT",
                                endpoint = self.server + endpoint,
                                data = data,
                                auth = self.credentials,
                                content = content)

    def delete(self, endpoint):
        """
        Sends a DELETE to endpoint.
        """
        response = self.request(method = "DELETE",
                                endpoint = self.server + endpoint,
                                auth = self.credentials)

    def get_inventory_nodes(self):
        endpoint = "/restconf/operational/opendaylight-inventory:nodes/"
        return self.get(endpoint)

    def get_nodes(self):
        inventory = self.get_inventory_nodes()
        nodes = inventory['nodes']['node']
        result = {}
        for node in nodes:
            obj = ODLNode(node, self)
            result[obj.id] = obj
        return result

    def get_node_by_id(self, id):
        nodes = self.get_nodes()
        try:
            return nodes[id]
        except KeyError:
            raise NodeNotFound("Node %s not found" % id)

    def get_connector_by_id(self, id):
        nodes = self.get_nodes()
        for node in nodes.values():
            connector = node.get_connector_by_id(id)
            if connector and connector.id == id:
                return connector
        return None
