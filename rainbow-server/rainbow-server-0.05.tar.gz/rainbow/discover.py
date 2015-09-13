# encoding=utf-8

import socket
import logging as log
import time
import traceback
import json
import sys

from tornado.httpclient import HTTPClient
from tornado.httpclient import HTTPRequest

import settings
from config import g_CONFIG
from config import g_Online_Server
from config import g_Online_Server_deque

g_udp_port_range = (2014, 2014 + settings.MAX_PORT)


def udp_listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    ok = False
    for udp_port in range(g_udp_port_range[0], g_udp_port_range[1]):
        try:
            s.bind(('', udp_port))
            log.info('udp_port = %d' % udp_port)
            ok = True
            break
        except Exception, e:
            log.debug(e)
    if not ok:
        log.error('not enough udp port')
        sys.exit(0)

    while True:
        try:
            data, addr = s.recvfrom(1024)
            try:
                data = json.loads(data)
                if data['msgtype'] in ['online', 'offline']:
                    http_port = data['port']
                else:
                    continue
            except Exception, e:
                log.warning(e)
                log.warning(traceback.format_exc())
                continue

            # 过滤自己，过滤不同集群
            if g_CONFIG['server_identity'] == data['server_identity'] or \
                    g_CONFIG['cluster_name'] != data['cluster_name']:
                continue
            else:
                remote_http = 'http://%s:%d' % (addr[0], http_port)
                try:
                    broadcast_hdl[data['msgtype']](remote_http)
                except Exception, e:
                    log.warning(e)
                    log.warning(traceback.format_exc())
        except Exception, e:
            log.error(e)
            log.error(traceback.format_exc())


def handle_online(remote_http):
    if not g_Online_Server.get(remote_http):
        url = '%s/hello/' % remote_http
        req = HTTPRequest(
            url=url, method='GET',
            connect_timeout=2, request_timeout=2)
        http_client = HTTPClient()
        rsp = http_client.fetch(req)
        if rsp.code == 200:
            g_Online_Server[remote_http] = time.time()
            g_Online_Server_deque.append(remote_http)
    else:
        g_Online_Server[remote_http] = time.time()

    log.debug(g_Online_Server)
    log.debug(g_Online_Server_deque)
    handle_expire()


def handle_offline(remote_http):
    try:
        g_Online_Server_deque.remove(remote_http)
    except:
        pass
    if g_Online_Server.get(remote_http):
        del g_Online_Server[remote_http]
    log.debug(g_Online_Server)
    log.debug(g_Online_Server_deque)


broadcast_hdl = {
    'online': handle_online,
    'offline': handle_offline}


def handle_expire():
    timenow = time.time()
    to_remove_list = []
    for remote_http in g_Online_Server_deque:
        timelast = g_Online_Server.get(remote_http, 0)
        if timenow - timelast > 30:
            to_remove_list.append(remote_http)

    for remote_http in to_remove_list:
        g_Online_Server_deque.remove(remote_http)
        if g_Online_Server.get(remote_http):
            del g_Online_Server[remote_http]


def broadcast_online():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    data = {
        'msgtype': 'online',
        'port': g_CONFIG['socket_port'],
        'server_identity': g_CONFIG['server_identity'],
        'cluster_name': g_CONFIG['cluster_name'],
    }
    msg = json.dumps(data)
    while True:
        try:
            for udp_port in range(g_udp_port_range[0], g_udp_port_range[1]):
                s.sendto(msg, ('<broadcast>', udp_port))
            time.sleep(10)
        except Exception, e:
            log.error(e)
            log.error(traceback.format_exc())
            time.sleep(10)


def broadcast_offline():
    log.info('i will be offline')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    data = {
        'msgtype': 'offline',
        'port': g_CONFIG['socket_port'],
        'server_identity': g_CONFIG['server_identity'],
        'cluster_name': g_CONFIG['cluster_name']
    }
    msg = json.dumps(data)
    for udp_port in range(g_udp_port_range[0], g_udp_port_range[1]):
        s.sendto(msg, ('<broadcast>', udp_port))
