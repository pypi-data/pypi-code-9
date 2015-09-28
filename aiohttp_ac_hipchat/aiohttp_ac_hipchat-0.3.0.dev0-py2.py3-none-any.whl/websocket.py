import asyncio
import asyncio_redis
from collections import defaultdict
import logging
from urllib.parse import urlparse
import aiohttp
from aiohttp import web
import json

log = logging.getLogger(__name__)

ws_connections = defaultdict(lambda: defaultdict(set))

class WebSocket:

    def __init__(self, redis_pool):
        self.redis_pool = redis_pool

    def publish(self, client_id, room_id, data):
        channel_key = "updates:{client_id}:{room_id}".format(client_id=client_id, room_id=room_id)
        log.debug("Publish update to Redis channel {0}".format(channel_key))

        nb_clients = yield from self.redis_pool.publish(channel_key, json.dumps({
            "client_id": client_id,
            "room_id": room_id,
            "data": data,
        }))
        log.debug("Published to {0} clients".format(nb_clients))

        return nb_clients

@asyncio.coroutine
def websocket_send_udpate(json_data):
    data = json.loads(json_data)

    ws_connections_for_room = ws_connections[data["client_id"]][data["room_id"]]
    log.debug("Send update to {0} WebSocket".format(len(ws_connections_for_room)))
    for ws_connection in ws_connections_for_room:
        try:
            ws_connection.send_str(json.dumps(data["data"]))
        except RuntimeError as e:
            log.warn(e)
            ws_connections.remove(ws_connection)

@asyncio.coroutine
def reader(subscriber):
    while True:
        reply = yield from subscriber.next_published()
        yield from websocket_send_udpate(reply.value)

@asyncio.coroutine
def init_pub_sub(app):
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

    connection = yield from asyncio_redis.Connection.create(host=url.hostname, port=url.port, password=url.password,
                                                            db=db)
    sub = yield from connection.start_subscribe()
    app["redis_sub"] = sub

    asyncio.async(reader(sub))

@asyncio.coroutine
def subscribe_new_client(app, client_id, room_id):
    chanel_key = "updates:{client_id}:{room_id}".format(client_id=client_id, room_id=room_id)
    log.debug("Subscribe to {0}".format(chanel_key))
    yield from app["redis_sub"].subscribe([chanel_key])

@asyncio.coroutine
def unsubscribe_client(app, client_id, room_id):
    chanel_key = "updates:{client_id}:{room_id}".format(client_id=client_id, room_id=room_id)
    log.debug("Unsubscribe to {0}".format(chanel_key))
    yield from app["redis_sub"].unsubscribe([chanel_key])

@asyncio.coroutine
def keep_alive(websocket, ping_period=15):
    while True:
        yield from asyncio.sleep(ping_period)

        try:
            websocket.ping()
        except Exception as e:
            log.debug('Got exception when trying to keep connection alive, '
                      'giving up.')
            return

@asyncio.coroutine
def websocket_handler(request):
    response = web.WebSocketResponse()
    ok, protocol = response.can_start(request)
    if not ok:
        return web.Response(text="Can't start webSocket connection.")

    response.start(request)

    asyncio.async(keep_alive(response))

    client_id = request.client.id
    room_id = request.jwt_data["context"]["room_id"]

    ws_connections_for_room = ws_connections[client_id][room_id]
    if len(ws_connections_for_room) == 0:
        yield from subscribe_new_client(request.app, client_id, room_id)

    ws_connections_for_room.add(response)
    log.debug("WebSocket connection open ({0} in total)".format(len(ws_connections)))

    while True:
        try:
            msg = yield from response.receive()

            if msg.tp == aiohttp.MsgType.close:
                log.info("websocket connection closed")
            elif msg.tp == aiohttp.MsgType.error:
                log.warn("response connection closed with exception %s",
                         response.exception())
        except RuntimeError:
            break

    ws_connections_for_room = ws_connections.get(client_id).get(room_id)
    ws_connections_for_room.remove(response)

    if len(ws_connections_for_room) == 0:
        yield from unsubscribe_client(request.app, client_id, room_id)

    return response

@asyncio.coroutine
def websocket_setup(app):
    addon = app["addon"]
    yield from init_pub_sub(app)

    app["websocket"] = WebSocket(app["redis_pool"])

    ws_handler = addon.require_jwt()(websocket_handler)

    app.router.add_route('GET', '/websocket', ws_handler)


