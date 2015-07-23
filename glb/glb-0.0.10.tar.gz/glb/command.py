import click
import datetime
from flask import Flask
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

import v1
from .settings import Config
from .sockethandler import Handler
from .core.extensions import redis


def create_app(config=None):
    app = Flask(__name__, static_folder='static')
    if config:
        app.config.update(config)
    else:
        app.config.from_object(Config)
    redis.init_app(app)
    if not redis.exists(Config.PORTS_NUMBER_COUNT_KEY):
        ''' init current port value can be assigned '''
        redis.set(Config.PORTS_NUMBER_COUNT_KEY, Config.PORT_RANGE[1])
    if not redis.exists(Config.LATEST_VERSION):
        redis.set(Config.LATEST_VERSION, str(datetime.datetime.now()))

    app.register_blueprint(
        v1.bp,
        url_prefix='/v1')
    return app


def wsgi_app(environ, start_response):
    path = environ['PATH_INFO']
    if path == '/websocket':
        Handler().handle_websocket(environ['wsgi.websocket'])
    else:
        return create_app()(environ, start_response)


@click.command()
@click.option('-h', '--host_port', type=(unicode, int),
              default=('0.0.0.0', 5000), help='Host and port of server.')
@click.option('-r', '--redis', type=(unicode, int, int),
              default=('127.0.0.1', 6379, 2),
              help='Redis url of server.')
@click.option('-p', '--port_range', type=(int, int),
              default=(50000, 61000),
              help='Port range to be assigned.')
def manage(host_port, redis=None, port_range=None):
    Config.REDIS_URL = 'redis://%s:%s/%s' % redis
    Config.PORT_RANGE = port_range
    http_server = WSGIServer(host_port,
                             wsgi_app, handler_class=WebSocketHandler)
    print '----GLB Server run at %s:%s-----' % host_port
    http_server.serve_forever()
