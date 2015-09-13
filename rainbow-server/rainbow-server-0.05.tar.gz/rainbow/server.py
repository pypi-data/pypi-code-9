# encoding=utf-8

import signal
import time
import settings
import logging as log
import thread
from hashlib import sha1
from uuid import uuid4
import socket

import tornado.web
import tornado.ioloop
from tornado.httpserver import HTTPServer

from wshandler import WebSocketHandler
from webhandler import SendMessageHandler
from webhandler import SubChannelHandler
from webhandler import UnSubChannelHandler
from webhandler import HelloHandler
from web.serverinfo import ServerInfoHandler
from web.serverinfo import UpdateConfigHandler
from discover import broadcast_online, broadcast_offline
from discover import udp_listen
from api import init_config

from config import g_CONFIG


if settings.DEBUG:
    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 1
else:
    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3

g_socket_port_range = (1984, 1984 + settings.MAX_PORT)

application = tornado.web.Application([
    # for websocket
    (r'/connect/', WebSocketHandler),

    # for HTTP
    (r'/send/', SendMessageHandler),
    (r'/sub/', SubChannelHandler),
    (r'/unsub/', UnSubChannelHandler),
    (r'/hello/', HelloHandler),
    (r'/serverinfo/', ServerInfoHandler),
    (r'/updateconfig/', UpdateConfigHandler),
])


def shutdown():
    log.info('Stopping http server')

    broadcast_offline()

    # 关闭本进程所有的客户端连接并将用户从在线列表中去掉。
    log.info('make all user offline')
    try:
        WebSocketHandler.shutdown()
    except Exception, e:
        log.error(e, exc_info=True)

    log.info('Will shutdown in %s seconds ...',
             MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()
    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            log.info('Shutdown')
    stop_loop()


def sig_handler(sig, frame):
    log.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def udp_handler():
    thread.start_new_thread(udp_listen, ())


def udp_send():
    thread.start_new_thread(broadcast_online, ())


def set_server_identity():
    local_ip = socket.gethostbyname(socket.gethostname())
    str_tmp = ''.join(
        [uuid4().get_hex(),
         local_ip,
         str(g_CONFIG['socket_port']),
         '%f' % time.time(),
         ])
    g_CONFIG['server_identity'] = sha1(str_tmp).hexdigest()


def main():
    ret = init_config()
    if not ret:
        log.error('config err, server exit')
        return

    socket_port = g_CONFIG.get('socket_port') or g_socket_port_range[0]

    server = HTTPServer(application)
    try:
        server.listen(socket_port)
    except:
        ok = False
        for port in range(g_socket_port_range[0], g_socket_port_range[1]):
            try:
                server.listen(port)
                ok = True
                socket_port = port
                break
            except Exception, e:
                log.debug(e)
        if not ok:
            log.info('http port is over, server exit')
            return
    g_CONFIG['socket_port'] = socket_port
    log.info('http port = %d' % socket_port)

    set_server_identity()

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    udp_handler()
    udp_send()
    tornado.ioloop.IOLoop.instance().start()

    log.info('server exit')

if __name__ == '__main__':
    main()
