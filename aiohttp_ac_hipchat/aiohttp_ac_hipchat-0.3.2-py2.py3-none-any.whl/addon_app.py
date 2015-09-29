import asyncio
from urllib.parse import urlparse
import logging
from aiohttp_ac_hipchat.addon import Addon

from aiohttp_ac_hipchat.cache import RedisCache
from aiohttp_ac_hipchat.store import MongoDBStore
from aiohttp_ac_hipchat.webapp import WebApp
import os
import asyncio_mongo
import asyncio_redis

_log = logging.getLogger(__name__)

def create_addon_app(addon_key=None, addon_name=None, from_name=None, debug=False,
        vendor_name=None, vendor_url=None,
        base_url="http://localhost:5000", addon_client_store=None, scopes=None, **kwargs):

    config = get_config(addon_key=addon_key,
                        addon_name=addon_name,
                        from_name=from_name,
                        debug=debug,
                        base_url=base_url,
                        vendor_name=vendor_name,
                        vendor_url=vendor_url)
    init_log(config["DEBUG"])

    loop = asyncio.get_event_loop()
    app = WebApp(loop=loop)

    app["config"] = config

    if not addon_client_store:
        mongodb = loop.run_until_complete(init_mongodb(config["MONGO_URL"]))
        app["mongodb"] = mongodb
        app["addon_client_store"] = MongoDBStore(mongodb)

    redis = loop.run_until_complete(init_redis(config["REDIS_URL"]))
    app["redis_pool"] = redis
    app["cache"] = RedisCache(redis)

    addon = init_addon(app, scopes)
    app['addon'] = addon

    return app, addon

@asyncio.coroutine
def init_mongodb(mongo_url="mongo://localhost:27017/test"):
    _log.info("Connecting to MongoDB %s" % mongo_url)
    c = yield from asyncio_mongo.Pool.create(url=mongo_url, poolsize=os.environ.get("MONGO_POOL_SIZE", 2))
    return c

@asyncio.coroutine
def init_redis(redis_url="redis://localhost:6379"):
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

def init_log(debug=False):
    if debug:
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

def init_addon(app, scopes):
    return Addon(app, scopes=scopes)

def get_config(addon_key=None, addon_name=None, from_name=None, debug=False, base_url="http://localhost:5000",
        vendor_name=None, vendor_url=None):
    return {
        "DEBUG": True if "true" == os.environ.get("DEBUG", "false") else debug,
        "ADDON_KEY": os.environ.get("ADDON_KEY", addon_key),
        "ADDON_NAME": os.environ.get("ADDON_NAME", addon_name),
        "ADDON_VENDOR_NAME": os.environ.get("ADDON_VENDOR_NAME", vendor_url),
        "ADDON_VENDOR_URL": os.environ.get("ADDON_VENDOR_URL", vendor_name),
        "ADDON_FROM_NAME": os.environ.get("ADDON_FROM_NAME", from_name),
        "BASE_URL": os.environ.get("BASE_URL", base_url).rstrip("\\"),
        "REDIS_URL": os.environ.get("REDIS_URL", "redis://localhost:6379"),
        "MONGO_URL": os.environ.get("MONGO_URL", "mongo://localhost:27017/test")
    }

