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

from flask import Response
from datetime import timedelta
from flask import request, current_app
from functools import update_wrapper

__author__ = 'Alexander Rüedlinger'
__all__ = ['cors', 'make_response']


SERIALIZERS = {
    'application/json': lambda obj: obj.to_json(),
    'application/xml': lambda obj: obj.to_xml(),
    'text/plain': lambda obj: obj.to_html(),
    'application/ld+json': lambda obj: obj.to_jsonld()
}


def cors(origin='*', methods=None, headers=None, max_age=2520):
    # source: http://flask.pocoo.org/snippets/56/

    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    else:
        methods = 'GET, OPTIONS'

    if headers is not None:
        headers = ', '.join(headers)
    else:
        headers = 'x-prototype-version,x-requested-with'

    from flask import make_response

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = methods
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Headers'] = headers

            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def make_response(obj, default='application/ld+json', status=200):
    cts = request.accept_mimetypes

    if cts:
        content_type, _ = cts[0]

        if content_type in SERIALIZERS:
            fun_serializer = SERIALIZERS[content_type]

            doc = fun_serializer(obj)
            return Response(response=doc, status=status, content_type=content_type)
        else:
            fun_serializer = SERIALIZERS[default]
            doc = fun_serializer(obj)
            return Response(response=doc, status=status, content_type=default)
    else:
        fun_serializer = SERIALIZERS[default]
        doc = fun_serializer(obj)
        return Response(response=doc, status=status, content_type=default)