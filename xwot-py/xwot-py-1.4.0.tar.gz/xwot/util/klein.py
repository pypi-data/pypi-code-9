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

from __future__ import absolute_import

__author__ = 'Alexander Rüedlinger'
__all__ = ['cors', 'make_response']

SERIALIZERS = {
    'application/json': lambda obj: obj.to_json(),
    'application/xml': lambda obj: obj.to_xml(),
    'text/plain': lambda obj: obj.to_html(),
    'application/ld+json': lambda obj: obj.to_jsonld()
}


def cors(request, origin='*', methods=None, max_age=2520, headers=None):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    else:
        methods = 'GET, OPTIONS'

    if headers is not None:
        headers = ', '.join(headers)
    else:
        headers = 'origin,x-prototype-version,x-requested-with,content-type,accept'

    request.setHeader('Access-Control-Allow-Origin', origin)
    request.setHeader('Access-Control-Allow-Methods', methods)
    request.setHeader('Access-Control-Allow-Headers', headers)
    request.setHeader('Access-Control-Max-Age', max_age)


def make_response(obj, request, default='application/ld+json', status=200):
    content_type = request.getHeader('Accept')

    if content_type in SERIALIZERS:
        fun_serializer = SERIALIZERS[content_type]
        doc = fun_serializer(obj)
        request.setHeader('Content-Type', content_type)
        request.setResponseCode(status)
        return doc
    else:
        fun_serializer = SERIALIZERS[default]
        doc = fun_serializer(obj)
        request.setHeader('Content-Type', default)
        request.setResponseCode(status)
        return doc