#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
import traceback
import threading
import json
import time
from datetime import timedelta
from werkzeug.routing import Map, Rule, RequestRedirect, BuildError
from werkzeug.exceptions import HTTPException

from easydict import EasyDict as edict

import pyokapi
from pyokapi import client, api

url_map = Map()
view_functions = {}

def _decorator(method):
    def d(rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            options["methods"] = (method,)
            #f = gen.coroutine(f)
            add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator
    return d

for m in ['get', 'post', 'put', 'delete']:
    setattr(pyokapi, m, _decorator(m))


def _endpoint_from_view_func(view_func):
    """Internal helper that returns the default endpoint for a given
    function.  This always is the function name.
    """
    assert view_func is not None, 'expected view func if endpoint ' \
                                  'is not provided.'
    return view_func.__name__
    
def add_url_rule(rule, endpoint=None, view_func=None, **options):
    if endpoint is None:
        endpoint = _endpoint_from_view_func(view_func)
    options['endpoint'] = endpoint
    methods = options.pop('methods', None)

    # if the methods are not given and the view_func object knows its
    # methods we can use that instead.  If neither exists, we go with
    # a tuple of only `GET` as default.
    if methods is None:
        methods = getattr(view_func, 'methods', None) or ('GET',)
    methods = set(methods)

    # Methods that should always be added
    required_methods = set(getattr(view_func, 'required_methods', ()))

    # starting with Flask 0.8 the view_func object can disable and
    # force-enable the automatic options handling.
    provide_automatic_options = getattr(view_func,
        'provide_automatic_options', None)

    if provide_automatic_options is None:
        if 'OPTIONS' not in methods:
            provide_automatic_options = True
            required_methods.add('OPTIONS')
        else:
            provide_automatic_options = False

    # Add the required methods now.
    methods |= required_methods

    # due to a werkzeug bug we need to make sure that the defaults are
    # None if they are an empty dictionary.  This should not be necessary
    # with Werkzeug 0.7
    options['defaults'] = options.get('defaults') or None

    rule = Rule(rule, methods=methods, **options)
    rule.provide_automatic_options = provide_automatic_options

    url_map.add(rule)
    if view_func is not None:
        old_func = view_functions.get(endpoint)
        if old_func is not None and old_func != view_func:
            raise AssertionError('View function mapping is overwriting an '
                                 'existing endpoint function: %s' % endpoint)
        view_functions[endpoint] = view_func
        
class Shortly(object):

    def __init__(self, url_map, view_func):
        self.url_map = url_map
        self.view_func = view_func

    def dispatch_request(self, request):
        api.args = request.args
        api.headers = request.headers
        api.body = request.data

        adapter = self.url_map.bind_to_environ(request.environ)

        try:
            endpoint, values = adapter.match()
            return view_func[endpoint](**values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app():
    app = Shortly(url_map)
    return app
    
if __name__ == '__main__':

    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 8750, create_app(), use_reloader=True)
