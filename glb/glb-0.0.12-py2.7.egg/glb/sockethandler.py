# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
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
    """manage requests from websocket client"""

    __metaclass__ = Singleton

    env = Environment(loader=PackageLoader('glb', 'templates'))

    def __init__(self):
        self.redis = redis.StrictRedis.from_url(Config.REDIS_URL)
        self.db = DB(self.redis)
        self.db.init_redis()

    def get_haproxy_config(self):
        '''
        get haproxy-cfg and ssl_certificate files(crts) from GLB
        '''
        def set_values():
            if entrypoint.get('certificate', None):
                frontends[port]['crts'].append((
                    entrypoint.get('domain', ''),
                    entrypoint.get('port', ''),
                    entrypoint.get('b_name', '')))
            if entrypoint.get('cipher', None):
                frontends[port]['ciphers'].append(
                    entrypoint.get('cipher', None))

        balancers = self.db.get_balancer_list()
        frontends = dict()
        all_entrypoints = list()
        frontend_ports = set()
        for b in balancers:
            port = int(b.frontend.port)
            frontend_ports.add(port)
            frontends[port] = dict(mode=b.frontend.protocol,
                                   b_name=b.name,
                                   acls=list(),
                                   crts=list(),
                                   ciphers=list())
            entrypoints = b.entrypoints
            entrypoints = [dict(dict(b_name=b.name), **(e_p.as_dict()))
                           for e_p in b.entrypoints]
            all_entrypoints.extend(entrypoints)
        crts = list()
        for entrypoint in all_entrypoints:
            port = int(entrypoint.get('port', 0))
            certificate = entrypoint.get('certificate', {})
            if port in frontend_ports:
                set_values()
            else:
                frontends[port] = dict(
                    mode=entrypoint.get('protocol', ''),
                    acls=list(),
                    crts=list(),
                    ciphers=list())
                set_values()
            if certificate:
                if 'cipher' in certificate.keys():
                    certificate.pop('cipher')
                crts.append(dict(
                    domain=entrypoint.get('domain', ''),
                    port=entrypoint.get('port', 0),
                    certificate=entrypoint.get('certificate', '')))
            else:
                frontends[port]['acls'].append(entrypoint)
            frontend_ports.add(port)
        frontend_ports = sorted(list(frontend_ports))
        backends = [dict(name=b.name, servers=b.backends) for b in balancers]
        template = self.env.get_template('haproxy-template.html')
        haproxy_cfg = template.render(frontends=frontends,
                                      frontend_ports=frontend_ports,
                                      backends=backends)
        return dict(haproxy_cfg=haproxy_cfg, crts=crts)

    def get_nginx_config(self):
        '''
        get haproxy-cfg and ssl_certificate files(crts) from GLB
        '''
        nginx_list = self.db.get_nginx_list()
        if not nginx_list:
            nginx_list = []
        template = self.env.get_template('nginx-template.html')
        nginx_conf = template.render(nginx_list=nginx_list)

        def wrapper_ssl_files():
            ssl_files = []
            for nginx in nginx_list:
                certificate = getattr(nginx.server, 'certificate', None)
                if certificate:
                    ssl_file = certificate
                    ssl_file['name'] = nginx.name
                    ssl_files.append(ssl_file)
            return ssl_files
        return dict(nginx_conf=nginx_conf, ssl_files=wrapper_ssl_files())

    def handle_websocket(self, ws):
        '''
        handle with the websocket client requests
        '''
        def send_back(flag_haproxy=False, flag_nginx=False):
            '''
            write back service(haproxy or nginx) configuration
            '''
            content = {}
            if flag_haproxy:
                content['haproxy'] = self.get_haproxy_config()
            if flag_nginx:
                content['nginx'] = self.get_nginx_config()
            try:
                ws.send(json.dumps(content))
            except WebSocketError:
                print 'WebSocketError: Socket is dead'
                gevent.GreenletExit()

        def listen():
            '''
            monitor the changes from redis db
            '''
            channel = self.redis.pubsub()
            channel.subscribe(Config.LISTEN_REDIS_CHANNEL)
            for msg in channel.listen():
                flag_haproxy = False
                flag_nginx = False
                publish_data = msg['data']
                if publish_data and isinstance(publish_data, str):
                    slave = dict(address=message['addr'])
                    #slave = SlaveModel.create(address=message['addr'])
                    if publish_data.startswith('haproxy'):
                        slave.update(dict(haproxy_version=publish_data))
                        #slave.haproxy_version = publish_data
                        flag_haproxy = True
                    elif publish_data.startswith('nginx'):
                        if message['nginx_switch']:
                            slave.update(dict(nginx_version=publish_data))
                            #slave.nginx_version = publish_data
                            flag_nginx = True
                    else:
                        pass
                    self.db.save_slave(slave)
                    send_back(flag_haproxy, flag_nginx)

        while True:
            try:
                message = ws.receive()
            except WebSocketError:
                break
            message = json.loads(message)
            slave = self.db.get_slave(address=message['addr'])
            if not slave:
                slave = SlaveModel.create(address=message['addr'])
            flag_haproxy = False
            flag_nginx = False

            def is_service_version_changed(service_version, sys_version):
                version = self.redis.get(getattr(Config, sys_version, ''))
                if getattr(slave, service_version, None) != version:
                    setattr(slave, service_version, version)
                    self.db.save_slave(slave)
                    return True

            if message['nginx_switch']:
                flag_nginx = is_service_version_changed(
                    'nginx_version', 'NGINX_LATEST_VERSION')
            flag_haproxy = is_service_version_changed(
                'haproxy_version', 'HAPROXY_LATEST_VERSION')
            if flag_haproxy or flag_nginx:
                send_back(flag_haproxy, flag_nginx)
            greenlet = gevent.spawn(listen)
            gevent.joinall([greenlet])
            greenlet.kill()
