#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# xwot.py - Python tools for the extended Web of Things
# Copyright (C) 2015  Alexander Rüedlinger
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = 'Alexander Rüedlinger'

from xwot.util.serializer import pretty_json
import logging

logger = logging.getLogger('hydra vocab builder')


class HydraBuilder(object):
    CONTEXT = {
        "vocab": "missing",
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "ApiDocumentation": "hydra:ApiDocumentation",
        "property": {
            "@id": "hydra:property",
            "@type": "@id"
        },
        "readonly": "hydra:readonly",
        "writeonly": "hydra:writeonly",
        "supportedClass": "hydra:supportedClass",
        "supportedProperty": "hydra:supportedProperty",
        "supportedOperation": "hydra:supportedOperation",
        "method": "hydra:method",
        "expects": {
            "@id": "hydra:expects",
            "@type": "@id"
        },
        "returns": {
            "@id": "hydra:returns",
            "@type": "@id"
        },
        "statusCodes": "hydra:statusCodes",
        "code": "hydra:statusCode",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "label": "rdfs:label",
        "description": "rdfs:comment",
        "domain": {
            "@id": "rdfs:domain",
            "@type": "@id"
        },
        "range": {
            "@id": "rdfs:range",
            "@type": "@id"
        },
        "subClassOf": {
            "@id": "rdfs:subClassOf",
            "@type": "@id"
        }
    }

    def __init__(self, annotator):
        self._annotator = annotator
        self._contexts = {}
        self._documentation = annotator.get_documentation()

    @property
    def documentation(self):
        return self._annotator.get_documentation()

    def build(self):
        return self._build_api_doc()

    def _build_api_doc(self):
        resources = self._visit_resources()
        new_context = self.CONTEXT.copy()
        new_context['vocab'] = self._documentation.apidoc_url + '#'

        if self._documentation is None:
            raise Exception

        api_doc = {
            '@context': new_context,
            '@id': self._documentation.apidoc_url,
            '@type': 'ApiDocumentation',
            'supportedClass': resources
        }

        jsonld_doc = pretty_json(api_doc)
        with open('test.json', 'w+') as f:
            f.write(jsonld_doc)

        return jsonld_doc

    def _visit_resources(self):
        resources = []

        for resource_key, resource in self._annotator.get_resources().items():
            self._contexts[resource_key] = {
                'vocab': self._documentation.apidoc_url
            }
            routes = self._annotator.get_routes(resource_key)
            props = self._annotator.get_properties(resource_key)
            supported_operations = self._visit_routes(resource, routes)
            supported_properties = self._visit_properties(resource, props)

            resource_dic = {
                '@id': resource.iri.__str__(),
                '@type': 'hydra:Class',
                'label': resource.name,
                'description': resource.description,
                'supportedOperation': supported_operations,
                'supportedProperty': supported_properties
            }

            resources.append(resource_dic)

        return resources

    def _visit_routes(self, resource, routes):
        route_dics = []
        for route_key, route in routes.items():
            operation = self._create_route_dic(route_key, route)
            route_dics.append(operation)

        return route_dics

    def _create_route_dic(self, route_key, route):
        route_dic = {
            '@id': "_:%s" % route_key,
            '@type': 'hydra:Operation',
            'method': route.method,
            'label': route.description,
            'description': route.description,
            'expects': route.expects.__str__(),
            'returns': route.returns.__str__(),
            'statusCodes': route.status_codes
        }
        return route_dic

    def _visit_properties(self, resource, props):
        properties = []
        for prop_key, prop in props.items():
            prop_def = self._visit_iri(resource, prop)
            prop_dic = {
                'property': prop_def,
                'hydra:title': prop_key,
                'hydra:description': prop.description,
                'required': prop.required,
                'readonly': prop.readonly,
                'writeonly': prop.writeonly
            }
            properties.append(prop_dic)

        return properties

    def _visit_iri(self, resource, prop):
        _iri = prop.iri.__str__()
        prop_def = _iri

        if len(prop.route_keys) > 0:
            _routes = self._annotator.get_routes_from_keys(prop.route_keys)
            operations = [self._create_route_dic(route.name, route) for route in _routes]
            _first_route = _routes[0]
            _range = _first_route.returns.__str__()
            _domain = resource.iri.__str__()

            prop_def = {
                '@id': _iri,
                '@type': 'hydra:Link',
                'label': prop.name,
                'description': prop.description,
                'domain': _domain,
                'range': _range,
                'supportedOperation': operations
            }

        return prop_def
