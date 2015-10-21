# -*- coding: utf-8 -*-
from .command import manage
#from flask import Flask
#from geventwebsocket.handler import WebSocketHandler
#from gevent.pywsgi import WSGIServer
#from .settings import Config
#from .sockethandler import handle_websocket
#from glb.core.extensions import redis

#import v1
#import datetime

''''
def create_app(config=None):
    app = Flask(__name__, static_folder='static')
    if config:
        app.config.update(config)
    else:
        app.config.from_object(Config)
    redis.init_app(app)
    if not redis.exists(Config.PORTS_NUMBER_COUNT_KEY):
        redis.set(Config.PORTS_NUMBER_COUNT_KEY, Config.PORT_RANGE[1])
    if not redis.exists(Config.LATEST_VERSION):
        redis.set(Config.LATEST_VERSION, str(datetime.datetime.now()))

    app.register_blueprint(
        v1.bp,
        url_prefix='/v1')
    return app
'''

#def wsgi_app(environ, start_response):
#    path = environ["PATH_INFO"]
#    if path == "/websocket":
#        handle_websocket(environ["wsgi.websocket"])
#    else:
#        return create_app()(environ, start_response)

#if __name__ == '__main__':
#    http_server = WSGIServer(('127.0.0.1', 5000),
#                             wsgi_app, handler_class=WebSocketHandler)
#    http_server.serve_forever()
