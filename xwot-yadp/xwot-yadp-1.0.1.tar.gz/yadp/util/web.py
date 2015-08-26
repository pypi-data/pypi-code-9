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

__author__ = 'Alexander Rüedlinger'
__all__ = ['Server', 'create_server']

import json
import urllib
import logging
from base64 import b64encode, b64decode
from urlparse import urlparse, parse_qs

from twisted.internet import reactor
from klein import Klein
import treq
from werkzeug.http import parse_options_header

from yadp.twisted import Client
from yadp.semantic import Client as SemanticClient
from yadp import get_public_frontend_path, get_public_frontend_file

from rdflib import Graph
from rdflib.namespace import NamespaceManager, Namespace

from .vsm import Engine, Corpus, Document
import re

logger = logging.getLogger('web-yadp')


def create_server(reactor=reactor, host='localhost', server_port=8080, yadp_port=2019):
    yadp_client = Client(reactor, port=yadp_port)
    semantic_client = SemanticClient(yadp_client=yadp_client)
    server = Server(host=host, port=server_port, semantic_client=semantic_client, yadp_client=yadp_client)
    return server


class Server(object):
    app = Klein()

    DEFAULT_PREFIXES = {
        'xwot': 'http://xwot.lexruee.ch/vocab/core#',
        'xwot-ext': 'http://xwot.lexruee.ch/vocab/core-ext#',
        'schema': 'http://schema.org/',
        'hydra': 'http://www.w3.org/ns/hydra/core#',
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    }

    XWOT = Namespace('http://xwot.lexruee.ch/vocab/core#')
    XWOT_EXT = Namespace('http://xwot.lexruee.ch/vocab/core-ext#')
    HYDRA = Namespace('http://www.w3.org/ns/hydra/core#')
    SCHEMA = Namespace('http://schema.org/')
    RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')

    NAMESPACE_MANAGER = NamespaceManager(Graph())
    NAMESPACE_MANAGER.bind('xwot', XWOT)
    NAMESPACE_MANAGER.bind('xwot-ext', XWOT_EXT)
    NAMESPACE_MANAGER.bind('hydra', HYDRA)
    NAMESPACE_MANAGER.bind('schema', SCHEMA)
    NAMESPACE_MANAGER.bind('rdf', RDF)
    NAMESPACE_MANAGER.bind('rdfs', RDFS)

    XWOT_EXT_ROOM_ADDRESS = 'http://xwot.lexruee.ch/vocab/core-ext#roomAddress'

    def __init__(self, host, port, semantic_client, yadp_client):
        self._host = host
        self._port = port
        self._semantic_yadp_client = semantic_client
        self._yadp_client = yadp_client
        self._semantic_yadp_client.browse()
        self._static_path = get_public_frontend_path()
        self._static_files = ['index.html', 'bundle.js', 'semantic.min.css', 'jquery.min.js']
        self._index_file = 'Not found!'

        with open(get_public_frontend_file('index.html'), 'r') as f:
            self._index_file = f.read()

    def _create_device_dic(self, device):
        key = b64encode(device.location)
        return {
            'id': key,
            'urn': device.urn,
            'url': device.location,
            'descriptionType': device.description.content_type,
            'links': [
                device.location,
                '/api/devices/',
                '/api/devices/' + key + '/description'
            ]
        }

    def _create_resource_dic(self, resource):
        key = b64encode(resource.url)
        return {
            'id': key,
            'type': resource.type,
            'name': resource.name,
            'description': resource.description,
            'url': resource.url,
            'links': [
                resource.url,
                '/api/resources'
            ]
        }

    def _create_resource_collection_dic(self, resources):
        _resources = []
        for resource in resources:
            key = b64encode(resource.url)
            _resources.append({
                'id': key,
                'type': resource.type,
                'name': resource.name,
                'description': resource.description,
                'room': resource.query_property(self.XWOT_EXT_ROOM_ADDRESS),
                'url': resource.url,
                'links': [
                    resource.url,
                    '/api/resources/' + key
                ]
            })

        return {
            'members': _resources,
            'links': '/api'
        }

    def _create_search_resource_collection_dic(self, resources):
        _resources = []
        for resource in resources:
            key = b64encode(resource.url)
            _resources.append({
                'id': key,
                'type': resource.type,
                'sim': resource.sim * 100,
                'name': resource.name,
                'description': resource.description,
                'room': resource.query_property(self.XWOT_EXT_ROOM_ADDRESS),
                'url': resource.url,
                'links': [
                    resource.url,
                    '/api/resources/' + key
                ]
            })

        return {
            'members': _resources,
            'links': '/api'
        }

    def _create_device_collection_dic(self, devices):
        _devices = []
        for device in devices:
            key = b64encode(device.location)
            _devices.append({
                'id': key,
                'urn': device.urn,
                'url': device.location,
                'descriptionType': device.description.content_type,
                'links': [
                    device.location,
                    '/api/devices/' + key,
                    '/api/devices/' + key + '/description'
                ]
            })

        return {
            'members': _devices,
            'links': '/api'
        }

    def _expand_iri(self, iri):
        expanded_iri = iri
        for key, val in self.DEFAULT_PREFIXES.items():
            if iri.startswith(key + ':'):
                expanded_iri = iri.replace(key + ':', val)

        return expanded_iri

    def _extract_iris(self, iri_param):
        return [iri.strip() for iri in iri_param.split(',')]

    def _extract_urns(self, urn_param):
        return [urn.strip() for urn in urn_param.split(',')]

    @app.route('/')
    def index(self, request):
        request.setHeader('Content-Type', 'text/html')
        return self._index_file

    @app.route('/public/<string:file>')
    def static(self, request, file=''):
        if file in self._static_files:
            data = ''
            with open(get_public_frontend_file(file), 'r') as f:
                data = f.read()
            return data
        return ''

    @app.route('/api')
    def api_index(self, request):
        request.setHeader('Content-Type', 'application/json')
        dic = {
            'name': 'Yadp RESTful API Server',
            'description': 'The Yadp RESTful API Server provides basic functionality '
                           'to query xWoT resources found in a local area network.',
            'links': [
                '/api/resources?iri=',
                '/api/devices?urn=',
                '/api/sparql?default-graph-uri=',
                '/api/search?query=',
                '/api/graph'
            ]
        }
        return json.dumps(dic, sort_keys=True, indent=4)

    @app.route('/api/devices/<string:key>/description')
    def single_device_description(self, request, key):
        url = b64decode(key)

        devices = [device for device in self._yadp_client.devices() if device.location == url]
        if len(devices):
            description = devices[0].description
            request.setHeader('Content-Type', description.content_type)
            return description.content
        else:
            request.setHeader('Content-Type', 'application/json')
            request.setResponseCode(404)
            return {}

    @app.route('/api/devices/<string:key>')
    def single_device(self, request, key):
        url = b64decode(key)
        request.setHeader('Content-Type', 'application/json')

        devices = [device for device in self._yadp_client.devices() if device.location == url]
        if len(devices):
            _device = self._create_device_dic(devices[0])
            return json.dumps(_device, sort_keys=True, indent=4)
        else:
            request.setResponseCode(404)
            return {}

    @app.route('/api/devices')
    def devices(self, request):
        request.setHeader('Content-Type', 'application/json')
        q = parse_qs(urlparse(request.uri).query)
        urn_param = q.get('urn', ['urn:xwot:*'])[0]

        urns = self._extract_urns(urn_param)

        expanded_urns = []
        for urn in urns:
            if not urn.startswith('urn:'):
                urn = "urn:%s" % urn
            expanded_urns.append(urn)

        devices = []
        for urn in expanded_urns:
            devices += self._yadp_client.discovered(urn=urn)

        dic = self._create_device_collection_dic(devices)
        return json.dumps(dic, sort_keys=True, indent=4)

    @app.route('/api/resources/<string:key>')
    def single_resource(self, request, key):
        url = b64decode(key)
        request.setHeader('Content-Type', 'application/json')

        resource = self._semantic_yadp_client.resource(url=url)

        if resource:
            _resource = self._create_resource_dic(resource)
            return json.dumps(_resource, sort_keys=True, indent=4)
        else:
            request.setResponseCode(404)
            return {}

    @app.route('/api/resources')
    def resources(self, request):
        request.setHeader('Content-Type', 'application/json')
        q = parse_qs(urlparse(request.uri).query)
        iri_param = q.get('iri', [])

        if len(iri_param):
            iri_param = iri_param[0]
            iris = self._extract_iris(iri_param)
            expanded_iris = [self._expand_iri(iri) for iri in iris]
            resources = {}
            for expanded_iri in expanded_iris:
                for resource in self._semantic_yadp_client.find_resources(expanded_iri):
                    resources[resource.url] = resource
            resources = resources.values()
        else:
            resources = self._semantic_yadp_client.resources()

        dic = self._create_resource_collection_dic(resources)
        return json.dumps(dic, sort_keys=True, indent=4)

    SPARQL_RESULT_TYPES = {
        'xml': 'application/sparql-results+xml',
        'json': 'application/sparql-results+json',
        'csv': 'application/sparql-results+csv',
        'txt': 'text/plain'
    }

    SPARQL_ACCEPTED_FORMATS = {
        'application/xml': 'xml',
        'application/json': 'json',
        'application/csv': 'csv',
        'application/tsv': 'tsv',
        'application/sparql-results+xml': 'xml',
        'application/sparql-results+json': 'json',
        'application/sparql-results+csv': 'csv',
        'text/plain': 'txt',
    }

    def _add_query_prefixes(self, query):
        prefixes = ''
        for key, val in self.DEFAULT_PREFIXES.items():
            prefixes += "PREFIX %s: <%s>\n" % (key, val)
        return prefixes + query

    def _parse_content_type(self, content_type):
        parse_options_header(content_type)
        if ';' in content_type:
            parts = content_type.split(';')
            return parts[0].strip()
        else:
            return content_type

    def _handle_local_sparql_request(self, query, request):
        query = self._add_query_prefixes(query)
        accept = request.getHeader('Accept')
        _format = 'json'

        if accept in self.SPARQL_ACCEPTED_FORMATS.keys():
            _format = self.SPARQL_ACCEPTED_FORMATS[accept]

        try:
            qres = self._semantic_yadp_client.sparql_query(query)
            data = qres.serialize(format=_format)
            request.setHeader('Content-Type', self.SPARQL_RESULT_TYPES[_format])
            return data
        except:
            request.setResponseCode(400)
            return {}

    GRAPH_ACCEPTED_FORMATS = {
        'application/xml': 'xml',
        'application/rdf+xml': 'xml',
        'application/ld+json': 'json-ld',
        'application/json': 'json-ld',
        'application/n-triples': 'nt',
        'text/turtle': 'turtle',
        'text/n3': 'n3'
    }

    def _create_base(self, url):
        res = urlparse(url)
        base = res.scheme + '://' + res.netloc
        return base

    def _handle_remote_sparql_query(self, url, query, request):
        accept = request.getHeader('Accept')
        proxy_accept = request.getHeader('X-Forwarded-Accept')

        def _handle_error(failure):
            logger.debug("error: %s" % failure.getErrorMessage())
            request.setResponseCode(400)
            return {}

        def _read_response(response):
            content_type = response.headers.getRawHeaders('Content-Type')[0]
            content_type = self._parse_content_type(content_type)

            if response.code == 200 and content_type in self.GRAPH_ACCEPTED_FORMATS:
                return response, content_type
            else:
                raise RuntimeError

        def _read_content(tup):
            def _return_tuple(content):
                return content, content_type

            response, content_type = tup
            d = treq.content(response)
            d.addCallback(_return_tuple)
            return d

        def _parse_content(tup, _url, _query):
            content, content_type = tup
            base = self._create_base(_url)
            _format_out = 'json'
            _format_in = self.GRAPH_ACCEPTED_FORMATS[content_type]

            if accept in self.SPARQL_ACCEPTED_FORMATS.keys():
                _format_out = self.SPARQL_ACCEPTED_FORMATS[accept]

            if _format_in == 'json-ld':  # base keyword is only allowed for json-ld
                g = Graph().parse(data=content, format=_format_in, base=base)
            else:
                g = Graph().parse(data=content, format=_format_in)

            if accept in self.SPARQL_ACCEPTED_FORMATS:
                qres = g.query(_query)
                data = qres.serialize(format=_format_out)
                request.setHeader('Content-Type', self.SPARQL_RESULT_TYPES[_format_out])
                return data
            else:
                request.setResponseCode(400)
                return {}

        d = treq.get(url, headers={'Accept': proxy_accept})
        d.addCallback(_read_response)
        d.addErrback(_handle_error)

        d.addCallback(_read_content)
        d.addErrback(_handle_error)

        d.addCallback(_parse_content, url, query)
        d.addErrback(_handle_error)

        return d

    SPAQRL_DEFAULT_GRAPH = ['/api/graph', '']

    @app.route('/api/sparql', methods=['GET'])
    def sparql_query_GET(self, request):
        q = parse_qs(urlparse(request.uri).query)
        _query = q.get('query', [])
        default_graph_uri = q.get('default-graph-uri', self.SPAQRL_DEFAULT_GRAPH)[0]

        if len(_query):
            query = _query[0]

            if default_graph_uri in self.SPAQRL_DEFAULT_GRAPH:
                return self._handle_local_sparql_request(query, request)
            elif default_graph_uri.startswith('http://'):
                deferred = self._handle_remote_sparql_query(default_graph_uri, query, request)
                return deferred
            else:
                request.setResponseCode(400)
                return {}
        else:
            request.setResponseCode(400)
            return {}

    SPARQL_REQUEST_CONTENT_TYPES = ['application/x-www-form-urlencoded', 'application/sparql-query']

    @app.route('/api/sparql', methods=['POST'])
    def sparql_query_POST(self, request):
        query = request.content.read()
        content_type = request.getHeader('Content-Type')
        content_type = self._parse_content_type(content_type)
        q = parse_qs(urlparse(request.uri).query)
        default_graph_uri = q.get('default-graph-uri', self.SPAQRL_DEFAULT_GRAPH)[0]

        if content_type not in self.SPARQL_REQUEST_CONTENT_TYPES:
            request.setResponseCode(400)
            return {}

        if content_type == 'application/x-www-form-urlencoded':
            query = urllib.unquote(query)

        if len(query):
            if default_graph_uri in self.SPAQRL_DEFAULT_GRAPH:
                return self._handle_local_sparql_request(query, request)
            elif default_graph_uri.startswith('http://'):
                deferred = self._handle_remote_sparql_query(default_graph_uri, query, request)
                return deferred
            else:
                request.setResponseCode(400)
                return {}
        else:
            request.setResponseCode(400)
            return {}

    GRAPH_RESULT_TYPES = {
        'xml': 'application/rdf+xml',
        'json-ld': 'application/ld+json',
        'turtle': 'text/turtle',
        'n3': 'text/n3',
        'nt': 'application/n-triples'
    }

    @app.route('/api/graph')
    def graph(self, request):
        accept = request.getHeader('Accept')
        _format = 'json-ld'
        if accept in self.GRAPH_ACCEPTED_FORMATS.keys():
            _format = self.GRAPH_ACCEPTED_FORMATS[accept]

        content_type = self.GRAPH_RESULT_TYPES[_format]
        request.setHeader('Content-Type', content_type)

        g = self._semantic_yadp_client.graph()
        g.namespace_manager = self.NAMESPACE_MANAGER

        out = g.serialize(format=_format)

        return out

    def _shorten_iri(self, iri):
        for key, val in self.DEFAULT_PREFIXES.items():
            if val in iri:
                return iri.replace(val, '')
        return iri

    def _split_uppercase(self, string):
        return re.sub(r'([a-z])([A-Z])', r'\1 \2', string)

    @app.route('/api/search', methods=['GET'])
    def search(self, request):
        request.setHeader('Content-Type', 'application/json')
        q = parse_qs(urlparse(request.uri).query)
        _query = q.get('query', [])
        _resources = []

        if len(_query):
            query = _query[0]
            query_terms = query.split()

            documents = []
            resources = {}
            for res in self._semantic_yadp_client.resources():
                resources[res.url] = res

                terms = []
                if len(res.type):
                    for iri in res.type:
                        fragment = self._shorten_iri(iri)
                        new_terms = self._split_uppercase(fragment).split()
                        terms += new_terms
                if res.name:
                    terms += res.name.split()

                if res.description:
                    terms += res.description.split()

                documents.append(Document(res.url, terms))

            corpus = Corpus(documents)
            engine = Engine(corpus)
            sim = engine.query(query_terms)
            for key in reversed(sorted(sim, key=sim.get)):
                r = resources[key]
                _sim = sim[key]
                if _sim:
                    r.sim = _sim
                    _resources.append(r)

        dic = self._create_search_resource_collection_dic(_resources)
        return json.dumps(dic, sort_keys=True, indent=4)

    def _handle_proxy_request(self, method, request, data=None, content_type=None):
        def _handle_error(failure):
            logger.debug("error: %s" % failure.getErrorMessage())
            request.setResponseCode(400)
            return {}

        def _read_response_headers(response):
            _content_type = response.headers.getRawHeaders('Content-Type')[0]
            _content_type = self._parse_content_type(_content_type)
            request.setHeader('Content-Type', _content_type)
            request.setResponseCode(response.code)
            return response

        accept = request.getHeader('Accept')
        q = parse_qs(urlparse(request.uri).query)
        url = q.get('url', [])

        if len(url):
            headers = {'Accept': accept}
            if content_type is not None:
                headers['Content-Type'] = content_type

            url = urllib.unquote(url[0])
            d = treq.request(method, url, data=data, headers=headers)
            d.addCallback(_read_response_headers)
            d.addErrback(_handle_error)
            d.addCallback(treq.content)
            d.addErrback(_handle_error)
            return d
        else:
            request.setResponseCode(400)
            return {}

    @app.route('/api/proxy', methods=['GET'])
    def proxy_GET(self, request):
        return self._handle_proxy_request('GET', request)

    @app.route('/api/proxy', methods=['OPTIONS'])
    def proxy_OPTIONS(self, request):
        return self._handle_proxy_request('OPTIONS', request)

    @app.route('/api/proxy', methods=['HEAD'])
    def proxy_HEAD(self, request):
        return self._handle_proxy_request('HEAD', request)

    @app.route('/api/proxy', methods=['PUT'])
    def proxy_PUT(self, request):
        data = request.content.read()
        content_type = request.getHeader('Content-Type')
        content_type = self._parse_content_type(content_type)
        return self._handle_proxy_request('PUT', request, data=data, content_type=content_type)

    @app.route('/api/proxy', methods=['POST'])
    def proxy_POST(self, request):
        data = request.content.read()
        content_type = request.getHeader('Content-Type')
        content_type = self._parse_content_type(content_type)
        return self._handle_proxy_request('POST', request, data=data, content_type=content_type)

    @app.route('/api/proxy', methods=['DELETE'])
    def proxy_DELETE(self, request):
        data = request.content.read()
        content_type = request.getHeader('Content-Type')
        content_type = self._parse_content_type(content_type)
        return self._handle_proxy_request('DELETE', request, data=data, content_type=content_type)

    def run(self):
        self.app.run(self._host, port=self._port)