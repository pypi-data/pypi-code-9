# -*- coding: utf-8 -*-

from umsgpack import dumps

from bottle import HTTPError, HTTPResponse, JSONPlugin, PluginError, response

class MsgPackPlugin(object):
    name = 'msgpack'
    api = 2

    def setup(self, app):
        for other in app.plugins:
            if isinstance(other, (MsgPackPlugin, JSONPlugin)):
                raise PluginError('MsgPack or JSONplugin already installed')

    def apply(self, callback, route):

        def wrapper(*args, **kwargs):
            try:
                rv = callback(*args, **kwargs)

            except HTTPError as e:
                rv = e

            if isinstance(rv, dict):
                msgpack_response = dumps(rv)
                response.content_type = 'application/msgpack'
                return msgpack_response

            elif isinstance(rv, HTTPResponse) and isinstance(rv.body, dict):
                rv.body = dumps(rv.body)
                rv.content_type = 'application/msgpack'
                return rv

        return wrapper

Plugin = MsgPackPlugin
