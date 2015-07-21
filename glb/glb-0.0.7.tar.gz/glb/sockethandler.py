# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis
import threading

from jinja2 import Environment, PackageLoader
from glb.core.db import DB
from glb.settings import Config
from glb.models.slave import Slave as SlaveModel

env = Environment(loader=PackageLoader('glb', 'templates'))
redis = redis.StrictRedis.from_url(Config.REDIS_URL)
db = DB(redis)


def get_cfg():
    '''
    @method use to get haproxy_cfg content
    '''
    balancers = db.get_balancer_list()
    frontends = {}
    all_entrypoints = []
    frontend_ports = set([])
    for b in balancers:
        port = int(b.frontend.port)
        frontend_ports.add(port)
        frontends[port] = {'mode': b.frontend.protocol,
                           'b_name': b.name,
                           'acls': [],
                           'crts': [],
                           'ciphers': []}
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
    template = env.get_template('haproxy-template.html')
    cfg = template.render(frontends=frontends,
                          frontend_ports=frontend_ports,
                          backends=backends)
    return dict(cfg=cfg, crts=crts)


def handle_websocket(ws):
    '''
    @method manage websocket for client requests
    '''
    while True:
        message = ws.receive()

        def listen():
            'To monitor the change of the redis '
            channel = redis.pubsub()
            channel.subscribe('glb:data_last_update_time')
            for msg in channel.listen():
                if msg['data'] and isinstance(msg['data'], str):
                    slave = SlaveModel(message, msg['data'])
                    db.save_slave(slave)
                    ws.send(get_cfg())

        slave = db.get_slave(address=message)
        version = str(redis.get(Config.LATEST_VERSION))
        if slave:
            if slave.sync_time != version:
                slave.sync_time = version if version else None
                db.save_slave(slave)
                ws.send(get_cfg())
            else:
                t = threading.Thread(target=listen)
                t.setDaemon(True)
                t.start()
        else:
            slave = SlaveModel(message, version)
            db.save_slave(slave)
            ws.send(get_cfg())
