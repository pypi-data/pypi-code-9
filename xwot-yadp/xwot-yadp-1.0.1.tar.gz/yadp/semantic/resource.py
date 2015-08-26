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

import json
from .vocab import SchemaOrg
from rdflib.namespace import RDF
from rdflib import URIRef
from rdflib import Graph, plugin
from rdflib.parser import Parser
import rdfextras
import logging

logger = logging.getLogger('resource')


class Visitor(object):

    def visit_resource(self, resource):
        raise NotImplementedError


class HTTPResource(object):

    def __init__(self, url):
        self._url = url
        self._allow = []
        self._children = []

    @property
    def url(self):
        return self._url

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, val):
        self._children = val

    def accept(self, visitor):
        return visitor.visit_resource(self)


class JSONLDResource(object):

    def __init__(self, url, data, graph):
        self._url = url
        self._graph = graph
        self._dic = json.loads(data)
        self._children = []

    def set(self, prop, value):
        self._dic[prop] = value

    def get(self, prop):
        return self._dic.get(prop, None)

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, val):
        self._children = val

    @property
    def graph(self):
        return self._graph

    def _query_property(self, iri, all=False):
        objects = [unicode(o) for (s, p, o) in self._graph.triples((URIRef(self._url), iri, None))]
        if all:
            return object
        else:
            if len(objects):
                return objects[0]
            return None

    def query_property(self, iri):
        if type(iri):
            iri = URIRef(iri)
        return self._query_property(iri)

    @property
    def type(self):
        return [unicode(s) for (s, p, o) in self._graph.triples((URIRef(self._url), RDF.type, None))]

    @property
    def name(self):
        return self._query_property(SchemaOrg.NAME)

    @property
    def description(self):
        return self._query_property(SchemaOrg.DESCRIPTION)

    @property
    def dict(self):
        return self._dic

    @property
    def url(self):
        return self._url


class DescriptionParser(object):

    DESCRIPTION_TYPE = URIRef('http://xwot.lexruee.ch/vocab/core#Description')

    def __init__(self, description):
        self._description = description
        self._resources = {}
        self._root = None

        g = Graph().parse(data=description, format='json-ld')
        self._description_graph = g
        self._parse()

    def _parse(self):
        self._parse_description()
        return self._root

    def _parse_predicate_knows(self, subject):
        triples = self._description_graph.triples((subject, SchemaOrg.KNOWS, None))
        http_resources = []

        for s, p, o in triples:
            http_resource = HTTPResource(url=str(o))
            http_resources.append(http_resource)
            self._resources[http_resource.url] = http_resource
            http_resource.children = self._parse_predicate_knows(o)

        return http_resources

    def _parse_description(self):
        _triples = self._description_graph.triples((None, RDF.type, self.DESCRIPTION_TYPE))
        triples = [s for (s, p, o) in _triples]
        description_iri = triples[0]

        _resources = self._parse_predicate_knows(description_iri)
        self._root = _resources[0]

    @property
    def resources(self):
        return self._resources

    @property
    def tree(self):
        return self._root

    @property
    def description_graph(self):
        return self._description_graph