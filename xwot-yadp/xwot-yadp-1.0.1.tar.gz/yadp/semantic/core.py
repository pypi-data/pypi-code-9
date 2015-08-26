#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Yadp  - Yet Another Discovery Protocol
# Copyright (C) 2015  Alexander Rüedlinger
#
# This file is part of Yadp.
#
# Yadp is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Yadp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Yadp.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

__author__ = 'Alexander Rüedlinger'

import logging
from urlparse import urlparse
from rdflib.namespace import RDF
from rdflib import URIRef
from rdflib import Graph, plugin
from rdflib.parser import Parser
import rdfextras
import treq
from .resource import JSONLDResource, DescriptionParser, Visitor

rdfextras.registerplugins()
logger = logging.getLogger('semantic-yadp')


class Client(object):

    class HTTPResourceTreeVisitor(Visitor):

        def __init__(self, client):
            self._client = client
            self._tree = None

        @property
        def tree(self):
            return self._tree

        def visit_resource(self, http_resource):
            if http_resource.url in self._client._resource_data:
                data = self._client._resource_data[http_resource.url]
                graph = self._client._resource_graphs[http_resource.url]
                _resource = JSONLDResource(url=http_resource.url, data=data, graph=graph)

                if self._tree is None:
                    self._tree = _resource

                _children = []
                for child in http_resource.children:
                    _child = child.accept(self)
                    if _child is not None:
                        _children.append(_child)

                _resource.children = _children
                return _resource
            return None

    JSONLD_CONTENT_TYPE = 'application/ld+json'
    URN_PATTERN = 'urn:xwot:*'

    def __init__(self, yadp_client):
        self._yadp_client = yadp_client

        # lookup tables
        self._description_data = {}
        self._description_graphs = {}  # descriptions as rdflib graph objects
        self._description_links = {}  # links in the descriptions
        self._resource_graphs = {}  # resources as rdflib graph objects
        self._http_resources = {}  # http resources objects
        self._resource_data = {}

        self._global_description_graph = Graph()
        self._global_resource_graph = Graph()

        # setup hook methods
        self._yadp_client.on_alive(self._hook_on_alive)
        self._yadp_client.on_response(self._hook_on_response)
        self._yadp_client.on_byebye(self._hook_on_byebye)
        self._yadp_client.on_update(self._hook_on_update)

    def browse(self, urn=URN_PATTERN):
        self._yadp_client.browse(urn=urn, accept=self.JSONLD_CONTENT_TYPE)

    def _hook_on_response(self, device, args):
        self._add_device(device)

    def _hook_on_alive(self, device, args):
        self._add_device(device)

    def _hook_on_update(self, device, args):
        self._remove_device(device)
        self._add_device(device)
        self._create_global_description_graph()

    def _hook_on_byebye(self, device, args):
        self._remove_device(device)
        self._create_global_description_graph()

    def _add_device(self, device):
        description = device.description

        if device.location not in self._description_links:
            self._description_links[device.location] = []

        if description.content_type == self.JSONLD_CONTENT_TYPE:
            description_parser = DescriptionParser(description.content)

            if device.location not in self._description_graphs:
                self._description_data[device.location] = description.content
                self._description_graphs[device.location] = description_parser.description_graph
                self._global_description_graph += description_parser.description_graph
                self._global_resource_graph += description_parser.description_graph

                for url, http_resource in description_parser.resources.copy().items():
                    self._http_resources[url] = http_resource
                    self._description_links[device.location].append(url)
                    self._fetch_resource(http_resource)

    def _remove_device(self, device):
        if device.location in self._description_graphs:
            for url in self._description_links[device.location]:
                if url in self._resource_data:
                    del self._resource_data[url]

                if url in self._resource_graphs:
                    del self._resource_graphs[url]

                if url in self._http_resources:
                    del self._http_resources[url]

            if device.location in self._description_links:
                del self._description_links[device.location]

            if device.location in self._description_graphs:
                del self._description_graphs[device.location]

    def _create_global_description_graph(self):
        self._global_description_graph = Graph()
        for key, graph in self._description_graphs.copy().items():
            self._global_description_graph += graph

    def _create_base(self, url):
        res = urlparse(url)
        base = res.scheme + '://' + res.netloc
        return base

    def _fetch_resource(self, http_resource):
        logger.debug("fetch resource: %s" % http_resource.url)

        def _handle_content(content, url):
            logger.debug("parse content: %s" % url)
            base = self._create_base(url)
            graph = Graph().parse(data=content, format='json-ld', base=base)
            self._resource_data[url] = content
            self._resource_graphs[url] = graph
            self._global_resource_graph += graph

        def _handle_response(response, url):
            content_type = response.headers.getRawHeaders('Content-Type')

            if response.code == 200 and self.JSONLD_CONTENT_TYPE in content_type:
                deferred_content = treq.content(response)
                deferred_content.addCallback(_handle_content, url)
                deferred_content.addErrback(_handle_error)

        def _handle_error(failure):
            logger.debug("error: %s" % failure.getErrorMessage())

        deferred_response = treq.get(url=http_resource.url, headers={'ACCEPT': self.JSONLD_CONTENT_TYPE})
        deferred_response.addCallback(_handle_response, http_resource.url)
        deferred_response.addErrback(_handle_error)

    def match_resources(self, predicate=None, object=None):
        _triples = [(_s, _p, _o) for (_s, _p, _o) in self._global_resource_graph.triples((None, predicate, object))]
        resources = []

        for (_subject, _predicate, _object) in _triples:
            url = str(_subject)
            if url in self._resource_data:
                # data = self._resource_data[url]
                # graph = self._resource_graphs[url]
                http_resource = self._http_resources[url]

                visitor = self.HTTPResourceTreeVisitor(self)
                http_resource.accept(visitor)

                resource = visitor.tree  # JSONLDResource(url=url, data=data, graph=graph)
                resources.append(resource)

        return resources

    def triples(self, subject=None, predicate=None, object=None):
        _triples = self._global_resource_graph.triples((subject, predicate, object))
        return [triple for triple in _triples]

    def resources(self):
        _resources = [self.resource(url) for url, http_resource in self._http_resources.items()]
        return [resource for resource in _resources if resource is not None]

    def resource(self, url):
        http_resource = self._http_resources.get(url, None)
        if http_resource:
            visitor = self.HTTPResourceTreeVisitor(self)
            http_resource.accept(visitor)
            resource = visitor.tree
            return resource
        return None

    def device(self, url):
        if url in self._description_data:
            data = self._description_data[url]
            graph = self._description_graphs[url]
            resource = JSONLDResource(url=url, data=data, graph=graph)
            return resource
        return None

    def devices(self):
        resources = []
        for url, _ in self._description_data:
            resource = self.device(url)
            if resource is not None:
                resources.append(resource)

        return resources

    def find_resources(self, iri):
        _iri = iri
        if _iri is not None:
            _iri = URIRef(_iri)

        resources = {}
        for resource in self.match_resources(predicate=RDF.type, object=_iri):
            resources[resource.url] = resource

        return resources.values()

    def sparql_query(self, query):
        return self._global_resource_graph.query(query)

    def graph(self):
        g = Graph()
        for triple in self._global_resource_graph:
            g.add(triple)
        return g

    def run(self, run_reactor=True):
        self._yadp_client.run(run_reactor=run_reactor)