# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis
import gevent
import gevent.monkey
gevent.monkey.patch_socket()
from geventwebsocket import WebSocketError

from jinja2 import Environment, PackageLoader
from glb.core.db import DB
from glb.settings import Config
from glb.models.slave import Slave as SlaveModel


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance


class Handler(object):
    """manage requests from websocket client """

    __metaclass__ = Singleton

    env = Environment(loader=PackageLoader('glb', 'templates'))

    def __init__(self):
        self.redis = redis.StrictRedis.from_url(Config.REDIS_URL)
        self.db = DB(self.redis)

    def get_cfg(self):
        '''
        @method use to get haproxy_cfg content
        '''
        balancers = self.db.get_balancer_list()
        frontends = dict()
        all_entrypoints = list()
        frontend_ports = set()
        for b in balancers:
            port = int(b.frontend.port)
            frontend_ports.add(port)
            frontends[port] = {'mode': b.frontend.protocol,
                               'b_name': b.name,
                               'acls': list(),
                               'crts': list(),
                               'ciphers': list()}
            entrypoints = b.entrypoints
            entrypoints = [dict(dict(b_name=b.name), **(e_p.as_dict()))
                           for e_p in b.entrypoints]
            all_entrypoints.extend(entrypoints)
        crts = []
        for entrypoint in all_entrypoints:
            if entrypoint['certificate']:
                crts.append(dict(domain=entrypoint['domain'],
                                 port=entrypoint['port'],
                                 certificate=entrypoint['certificate']))
            port = int(entrypoint['port'])
            if port in frontend_ports:
                frontends[port]['acls'].append(entrypoint)
                if entrypoint['certificate']:
                    frontends[port]['crts'].append(
                        (entrypoint['domain'], entrypoint['port'],
                         entrypoint['b_name']))
                if entrypoint['cipher']:
                    frontends[port]['ciphers'].append(entrypoint['cipher'])
            else:
                frontends[port] = {'mode': entrypoint['protocol'],
                                   'acls': [],
                                   'crts': [],
                                   'ciphers': []}
                frontends[port]['acls'].append(entrypoint)
                if entrypoint['certificate']:
                    frontends[port]['crts'].append(
                        (entrypoint['domain'], entrypoint['port'],
                         entrypoint['b_name']))
                if entrypoint['cipher']:
                    frontends[port]['ciphers'].append(entrypoint['cipher'])
            frontend_ports.add(port)
        frontend_ports = sorted(list(frontend_ports))
        backends = [{'name': b.name, 'servers': b.backends} for b in balancers]
        template = self.env.get_template('haproxy-template.html')
        cfg = template.render(frontends=frontends,
                              frontend_ports=frontend_ports,
                              backends=backends)
        return dict(cfg=cfg, crts=crts)

    def handle_websocket(self, ws):
        '''
        @method manage websocket for client requests
        '''
        def listen():
            'To monitor the change of the redis '
            channel = self.redis.pubsub()
            channel.subscribe(Config.LISTEN_REDIS_CHANNEL)
            for msg in channel.listen():
                if msg['data'] and isinstance(msg['data'], str):
                    slave = SlaveModel(message, msg['data'])
                    self.db.save_slave(slave)
                    send()

        def send():
            try:
                ws.send(self.get_cfg())
            except WebSocketError:
                print 'WebSocketError: Socket is dead'
                raise gevent.GreenletExit()

        while True:
            try:
                message = ws.receive()
            except WebSocketError:
                break
            slave = self.db.get_slave(address=message)
            version = str(self.redis.get(Config.LATEST_VERSION))
            if slave:
                if slave.sync_time != version:
                    slave.sync_time = version if version else None
                    self.db.save_slave(slave)
                    send()
            else:
                slave = SlaveModel(message, version)
                self.db.save_slave(slave)
                send()
            greenlet = gevent.spawn(listen)
            gevent.joinall([greenlet])
            greenlet.kill()
