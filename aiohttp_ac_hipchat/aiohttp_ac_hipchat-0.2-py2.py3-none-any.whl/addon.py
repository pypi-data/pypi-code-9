import asyncio
from aiohttp_ac_hipchat.webapp import WebApp
from urllib.parse import urlparse
from aiohttp import web
from aiohttp_ac_hipchat.installable import add_installable_handlers
from aiohttp_ac_hipchat.oauth2 import Oauth2Client
import logging
from functools import wraps
import jwt
import os
import asyncio_mongo
import asyncio_redis

_log = logging.getLogger(__name__)


def create_addon_app(plugin_key=None, addon_name=None, from_name=None, debug=False,
        base_url="http://localhost:5000", scopes=None, **kwargs):
    config = {
        "DEBUG": True if "true" == os.environ.get("DEBUG", "false") else debug,
        "PLUGIN_KEY": os.environ.get("PLUGIN_KEY", plugin_key),
        "ADDON_NAME": os.environ.get("ADDON_NAME", addon_name),
        "FROM_NAME": os.environ.get("FROM_NAME", from_name),
        "BASE_URL": os.environ.get("BASE_URL", base_url).rstrip("\\"),
        "REDIS_URL": os.environ.get("REDIS_URL", "redis://localhost:6379"),
        "MONGO_URL": os.environ.get("MONGO_URL", "mongo://localhost:27017/test")
    }

    app = WebApp(middlewares=[config_middleware_factory(config),
                              redis_middleware,
                              mongodb_middleware,
                              addon_middleware])

    add_installable_handlers(app, scopes=scopes)

    return app


def hook_middleware_factory(app, handler):
    @asyncio.coroutine
    def middleware(request):
        if app.get("first_request", True):
            app["first_request"] = False

        return (yield from handler(request))

    return middleware


def config_middleware_factory(config):
    @asyncio.coroutine
    def config_middleware(app, handler):
        @asyncio.coroutine
        def middleware(request):
            app_config = app.get('config')
            if not app_config:
                app['config'] = app_config = config
                request.app['config'] = app_config

            return (yield from handler(request))

        return middleware

    return config_middleware


@asyncio.coroutine
def redis_middleware(app, handler):
    @asyncio.coroutine
    def init_redis():
        redis_url = app['config'].get('REDIS_URL')
        if not redis_url:
            redis_url = 'redis://localhost:6379'

        url = urlparse(redis_url)

        db = 0
        try:
            if url.path:
                db = int(url.path.replace('/', ''))
        except (AttributeError, ValueError):
            pass

        _log.info("Connecting to Redis %s" % redis_url)
        pool = yield from asyncio_redis.Pool.create(host=url.hostname, port=url.port, password=url.password,
                                                    db=db, poolsize=os.environ.get("REDIS_POOL_SIZE", 2))

        return pool

    @asyncio.coroutine
    def middleware(request):
        redis_pool = app.get('redis_pool')
        if not redis_pool:
            app['redis_pool'] = redis_pool = yield from init_redis()
            request.app['redis_pool'] = redis_pool

        return (yield from handler(request))

    return middleware


@asyncio.coroutine
def mongodb_middleware(app, handler):
    @asyncio.coroutine
    def init_mongodb():
        mongo_url = app['config'].get('MONGO_URL')
        if not mongo_url:
            mongo_url = 'mongo://localhost:27017/test'

        _log.info("Connecting to MongoDB %s" % mongo_url)
        c = yield from asyncio_mongo.Pool.create(url=mongo_url, poolsize=2)
        return c

    @asyncio.coroutine
    def middleware(request):
        mongodb = app.get('mongodb')
        if not mongodb:
            app['mongodb'] = mongodb = yield from init_mongodb()
            request.app['mongodb'] = mongodb

        return (yield from handler(request))

    return middleware


@asyncio.coroutine
def addon_middleware(app, handler):
    @asyncio.coroutine
    def init_addon():
        if app['config'].get('DEBUG', False):
            # You must initialize logging, otherwise you'll not see debug output.
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            aio_log = logging.getLogger("asyncio")
            aio_log.setLevel(logging.INFO)
            aio_log.propagate = True
        else:
            logging.basicConfig()
            aio_log = logging.getLogger("asyncio")
            aio_log.setLevel(logging.WARN)
            logging.getLogger().setLevel(logging.INFO)

        return Addon(app)

    @asyncio.coroutine
    def middleware(request):
        addon = app.get('addon')
        if not addon:
            app['addon'] = addon = yield from init_addon()
            request.app['addon'] = addon

        return (yield from handler(request))

    return middleware


class Addon(object):
    def __init__(self, app):
        self.mongodb = app['mongodb']
        self.redis_pool = app['redis_pool']
        self.events = {}

    @asyncio.coroutine
    def load_client(self, client_id):
        client_data = yield from self.mongodb.default_database.clients.find_one(Oauth2Client(client_id).id_query)
        if client_data:
            return Oauth2Client.from_map(client_data)
        else:
            return None

    def fire_event(self, name, obj):
        listeners = self.events.get(name, [])
        for listener in listeners:
            try:
                yield from listener(obj)
            except:
                logging.exception("Unable to fire event {name} to listener {listener}".format(
                    name=name, listener=listener
                ))

    def register_event(self, name, func):
        _log.debug("Registering event: " + name)
        self.events.setdefault(name, []).append(func)

    def unregister_event(self, name, func):
        del self.events.setdefault(name, [])[func]

    def event_listener(self, func):
        self.register_event(func.__name__, func)
        return func


@asyncio.coroutine
def validate_jwt(addon, request):
    signed_request = request.GET.get('signed_request', None) or \
        request.headers.get("x-acpt") or \
        request.headers.get("authorization")

    if not signed_request:
        return None, None, None

    oauth_id = jwt.decode(signed_request, verify=False)['iss']
    client = yield from addon.load_client(oauth_id)
    if not client:
        return None, None, None

    data = jwt.decode(signed_request, client.secret)
    return client, data, signed_request


def require_jwt(app):
    def require_jwt_inner(func):
        @asyncio.coroutine
        @wraps(func)
        def inner(*args, **kwargs):
            _log.debug("Validating jwt")
            request = args[0]
            client, data, signed_request = yield from validate_jwt(app['addon'], request)
            if client:
                request.client = client
                request.jwt_data = data
                request.signed_request = signed_request
                return (yield from func(*args, **kwargs))
            else:
                return web.HTTPUnauthorized(text="Unauthorized request, please check the JWT token")

        return inner

    return require_jwt_inner
