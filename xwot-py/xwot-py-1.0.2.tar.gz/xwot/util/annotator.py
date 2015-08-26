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

from xwot.util.vocab import NullIri


class Resource(object):
    def __init__(self, cls, description=None, iri=None, route_keys=None):
        self._cls = cls
        self._properties = {}
        self._description = description or ''
        self._route_keys = route_keys or []
        self._iri = iri or NullIri()

    @property
    def description(self):
        return self._description

    @property
    def iri(self):
        return self._iri

    @property
    def name(self):
        return self._cls.__name__

    @property
    def route_keys(self):
        return self._route_keys

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        self._properties = value


class Property(object):
    def __init__(self, name, iri, description, route_keys, required, readonly,
                 writeonly, range):
        self._name = name
        self._range = range
        self._description = description
        self._iri = iri or NullIri()
        self._route_keys = route_keys or []
        self._required = required
        self._readonly = readonly
        self._writeonly = writeonly

    @property
    def iri(self):
        return self._iri

    @property
    def range(self):
        return self._range

    @property
    def name(self):
        return self._name

    @property
    def writeonly(self):
        return self._writeonly

    @property
    def readonly(self):
        return self._readonly

    @property
    def required(self):
        return self._required

    @property
    def route_keys(self):
        return self._route_keys

    @property
    def description(self):
        return self._description

    @property
    def description(self):
        return self._description


class Route(object):
    def __init__(self, name, method, description=None, returns=None, status_codes=None, expects=None):
        self._name = name
        self._method = method
        self._description = description


        if status_codes is None:
            self._status_codes = []
        else:
            self._status_codes = status_codes

        self._expects = expects or NullIri()
        self._returns = returns or NullIri()

    @property
    def name(self):
        return self._name

    @property
    def method(self):
        return self._method

    @property
    def description(self):
        return self._description

    @property
    def returns(self):
        return self._returns

    @property
    def status_codes(self):
        return self._status_codes

    @property
    def expects(self):
        return self._expects


class Documentation(object):
    def __init__(self, apidoc_url='', title=None, description=None, entrypoint=None):
        self._title = title
        self._description = description
        self._apidoc_url = apidoc_url
        self._entrypoint = entrypoint

    @property
    def title(self):
        return self._title

    @property
    def apidoc_url(self):
        return self._apidoc_url

    @property
    def description(self):
        return self._description

    @property
    def entrypoint(self):
        return self._entrypoint


class Annotator(object):

    def __init__(self):
        self._documentation = None
        self._resources = {}
        self._routes = {}
        self._props = {}

    def documentation(self, apidoc_url, title=None, description=None, entrypoint=None):
        self._documentation = Documentation(apidoc_url=apidoc_url, title=title, description=description,
                                            entrypoint=entrypoint)

    def property(self, iri, description=None, routes=None, required=None, readonly=None, writeonly=None,
                 range=None):
        def decorator(meth):
            _prop = Property(name=meth.__name__, iri=iri, description=description, route_keys=routes,
                             required=required, readonly=readonly, writeonly=writeonly, range=range)
            self._props[meth.__name__] = _prop
            return meth

        return decorator

    def resource(self, iri, description=None, routes=None):
        def decorator(cls):
            _resource = Resource(cls=cls, description=description, iri=iri, route_keys=routes)
            _resource.properties = self._props

            self._props = {}
            self._resources[cls.__name__] = _resource
            return cls

        return decorator

    def route(self, name, method, description=None, returns=None, status_codes=None, expects=None):
        self._routes[name] = Route(name=name, method=method, description=description, returns=returns,
                                   expects=expects, status_codes=status_codes)
        def decorator(route_rule):
            return route_rule

        return decorator

    def get_resources(self):
        return self._resources

    def routes(self):
        return self._routes

    def get_properties(self, resource_key):
        if resource_key in self._resources:
            return self._resources[resource_key].properties
        return {}

    def get_routes(self, resource_key):
        if resource_key in self._resources:
            route_keys = self._resources[resource_key].route_keys
            return {route_key: route for (route_key, route) in self._routes.items() if route_key in route_keys}
        return {}

    def get_routes_from_keys(self, route_keys):
        return [route for key, route in self._routes.items() if key in route_keys]

    def get_documentation(self):
        return self._documentation