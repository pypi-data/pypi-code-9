# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime
from redis.exceptions import WatchError
from glb.settings import Config
from glb.models.slave import Slave as SlaveModel
from glb.models.balancer import Balancer as BalancerModel
from glb.models.backend import Backend as BackendModel
from glb.models.frontend import Frontend as FrontendModel
from glb.models.entrypoint import Entrypoint as EntrypointModel
from glb.models.nginx import (Nginx as NginxModel,
                              Upstream as UpstreamModel,
                              Server as ServerModel)


class DB(object):

    def __init__(self, redis):
        self.redis = redis

    def init_redis(self):
        if not self.redis.exists(Config.PORTS_NUMBER_COUNT_KEY):
            self.redis.set(Config.PORTS_NUMBER_COUNT_KEY, Config.PORT_RANGE[1])
        if not self.redis.exists(Config.HAPROXY_LATEST_VERSION):
            self.redis.set(Config.HAPROXY_LATEST_VERSION,
                           '%s_%s' % ('haproxy', str(datetime.datetime.now())))
        if not self.redis.exists(Config.NGINX_LATEST_VERSION):
            self.redis.set(Config.NGINX_LATEST_VERSION,
                           '%s_%s' % ('nginx', str(datetime.datetime.now())))

    def update_service_latest_version(self, service_name):
        latest_version = '%s_%s' % (service_name, str(datetime.datetime.now()))
        self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
        self.redis.set(getattr(Config, '%s_%s' %
                               (service_name.upper(), 'LATEST_VERSION')),
                       latest_version)

    def get_balancer(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            balancer = BalancerModel.create(
                name=balancer_name,
                frontend=self.get_frontend(balancer_name),
                backends=self.get_backend_list(balancer_name),
                entrypoints=self.get_entrypoint_list(balancer_name))
            return balancer

    def get_frontend(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            base_key = '%s:%s' % (FrontendModel.__prefix_key__, balancer_name)
            mapping = self.redis.hgetall(base_key)
            if 'port' in mapping.keys():
                mapping['port'] = eval(mapping['port'])
            frontend = FrontendModel.create(**mapping)
            return frontend

    def get_slave(self, address):
        if self.redis.sismember(SlaveModel.__prefix_key__, address):
            base_key = '%s:%s' % (SlaveModel.__prefix_key__, address)
            mapping = self.redis.hgetall(base_key)
            mapping.update(dict(address=address))
            slave = SlaveModel.create(**mapping)
            return slave

    def get_prefixed_balancer_names(self, prefix):
        b_names = self.redis.smembers(BalancerModel.__prefix_key__)
        result = [b_name for b_name in b_names if b_name.startswith(prefix)]
        return result

    def get_balancer_list(self):
        b_names = self.redis.smembers(BalancerModel.__prefix_key__)
        result = [self.get_balancer(b_name) for b_name in b_names]
        return result

    def get_backend_list(self, balancer_name):
        result = []
        backends_key = '%s:%s' % (balancer_name, BackendModel.__prefix_key__)
        b_ids = self.redis.smembers(backends_key)
        for b_id in b_ids:
            base_key = '%s:%s:%s' % (BackendModel.__prefix_key__,
                                     balancer_name, b_id)
            mapping = self.redis.hgetall(base_key)
            addr_port = b_id.split(':')
            mapping.update(dict(address=addr_port[0],
                                port=addr_port[1]))
            backend = BackendModel.create(**mapping)
            result.append(backend)
        return result

    def get_entrypoint_list(self, balancer_name):
        result = []
        entrypoints_key = '%s:%s' % (balancer_name,
                                     EntrypointModel.__prefix_key__)
        e_ids = self.redis.smembers(entrypoints_key)
        for e_id in e_ids:
            base_key = '%s:%s:%s' % (EntrypointModel.__prefix_key__,
                                     balancer_name, e_id)
            mapping = self.redis.hgetall(base_key)
            if 'certificate' in mapping.keys() and mapping['certificate']:
                mapping['certificate'] = json.loads(mapping['certificate'])
            addr_port = e_id.split(':')
            mapping.update(dict(domain=addr_port[0],
                                port=addr_port[1]))
            entrypoint = EntrypointModel.create(**mapping)
            result.append(entrypoint)
        return result

    def get_slave_list(self):
        result = []
        slaves = self.redis.smembers(SlaveModel.__prefix_key__)
        for address in slaves:
            slave = self.get_slave(address)
            result.append(slave)
        return result

    def save_balancer(self, balancer):
        if isinstance(balancer, BalancerModel):
            self.redis.sadd(balancer.__prefix_key__, balancer.name)
            self.save_frontend(balancer.frontend, balancer.name)
            for backend in balancer.backends:
                self.save_or_update_backend(backend, balancer.name)
            for entrypoint in balancer.entrypoints:
                self.save_or_update_entrypoint(entrypoint, balancer.name)
            return balancer

    def save_frontend(self, frontend, balancer_name):
        """ port decided by GLB """
        if isinstance(frontend, FrontendModel) and self.redis.sismember(
                BalancerModel.__prefix_key__, balancer_name):
            base_key = '%s:%s' % (frontend.__prefix_key__, balancer_name)
            mapping = frontend.as_dict()
            mapping.pop('port')
            self.redis.hmset(base_key, mapping)
            f = self.get_frontend(balancer_name)
            if not getattr(f, 'port', None):
                pipe = self.redis.pipeline()
                try:
                    pipe.watch(Config.PORTS_NUMBER_COUNT_KEY)
                    v = int(self.redis.get(Config.PORTS_NUMBER_COUNT_KEY))
                    if v > Config.PORT_RANGE[0]:
                        pipe.decr(Config.PORTS_NUMBER_COUNT_KEY)
                        pipe.hset(base_key, 'port', v)
                        pipe.execute()
                        setattr(frontend, 'port', v)
                except WatchError:
                    pass
            return frontend

    def update_frontend(self, frontend, balancer_name):
        if isinstance(frontend, FrontendModel) and self.redis.sismember(
                BalancerModel.__prefix_key__, balancer_name):
            base_key = '%s:%s' % (frontend.__prefix_key__, balancer_name)
            mapping = frontend.as_dict()
            mapping.pop('port')
            self.redis.hmset(base_key, mapping)
            return True
        return False

    def save_or_update_backend(self, backend, balancer_name):
        ''' use backend address and port as id '''
        if isinstance(backend, BackendModel) and self.redis.sismember(
                BalancerModel.__prefix_key__, balancer_name):
            backend_id = '%s:%s' % (backend.address, backend.port)
            base_key = '%s:%s:%s' % (backend.__prefix_key__,
                                     balancer_name, backend_id)
            mapping = backend.as_dict()
            mapping.pop('address')
            mapping.pop('port')
            self.redis.hmset(base_key, mapping)
            backends_key = '%s:%s' % (balancer_name, backend.__prefix_key__)
            self.redis.sadd(backends_key, backend_id)
            return backend

    def save_or_update_entrypoint(self, entrypoint, balancer_name):
        if isinstance(entrypoint, EntrypointModel) and self.redis.sismember(
                BalancerModel.__prefix_key__, balancer_name):
            e_id = '%s:%s' % (entrypoint.domain, entrypoint.port)
            base_key = '%s:%s:%s' % (entrypoint.__prefix_key__,
                                     balancer_name, e_id)
            mapping = entrypoint.as_dict()
            mapping.pop('domain')
            mapping.pop('port')
            if 'certificate' in mapping.keys() and mapping['certificate']:
                mapping['certificate'] = json.dumps(mapping['certificate'])
            else:
                mapping.pop('certificate')
            self.redis.hmset(base_key, mapping)
            entrypoints_key = '%s:%s' % (balancer_name,
                                         entrypoint.__prefix_key__)
            self.redis.sadd(entrypoints_key, e_id)
            return entrypoint

    def save_slave(self, slave):
        """use address as id"""
        if isinstance(slave, SlaveModel):
            base_key = '%s:%s' % (slave.__prefix_key__, slave.address)
            mapping = slave.as_dict()
            mapping.pop('address')
            self.redis.hmset(base_key, mapping)
            self.redis.sadd(slave.__prefix_key__, slave.address)
        return slave

    def delete_balancer(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            self.delete_frontend(balancer_name)
            self.delete_all_backend(balancer_name)
            self.delete_all_entrypoint(balancer_name)
            self.redis.srem(BalancerModel.__prefix_key__, balancer_name)
            return True
        return False

    def delete_frontend(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            base_key = '%s:%s' % (FrontendModel.__prefix_key__, balancer_name)
            self.redis.delete(base_key)
            return True
        return False

    def delete_backend(self, balancer_name, address, port):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            backends_key = '%s:%s' % (balancer_name,
                                      BackendModel.__prefix_key__)
            b_id = '%s:%s' % (address, port)
            rm_state = self.redis.srem(backends_key, b_id)
            base_key = '%s:%s:%s' % (BackendModel.__prefix_key__,
                                     balancer_name, b_id)
            if rm_state:
                self.redis.delete(base_key)
                return True
        return False

    def delete_backend_by_tag(self, balancer_name, tag):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            backends_key = '%s:%s' % (balancer_name,
                                      BackendModel.__prefix_key__)
            b_ids = self.redis.smembers(backends_key)
            for b_id in b_ids:
                base_key = '%s:%s:%s' % (BackendModel.__prefix_key__,
                                         balancer_name, b_id)
                r_tag = self.redis.hget(base_key, 'tag')
                if r_tag == tag:
                    self.redis.delete(base_key)
                    self.redis.srem(backends_key, b_id)
            return True
        return False

    def delete_all_backend(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            backends_key = '%s:%s' % (balancer_name,
                                      BackendModel.__prefix_key__)
            b_ids = self.redis.smembers(backends_key)
            for b_id in b_ids:
                base_key = '%s:%s:%s' % (BackendModel.__prefix_key__,
                                         balancer_name, b_id)
                self.redis.delete(base_key)
            self.redis.delete(backends_key)
            return True
        return False

    def delete_entrypoint(self, balancer_name, domain, port):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            entrypoints_key = '%s:%s' % (balancer_name,
                                         EntrypointModel.__prefix_key__)
            e_id = '%s:%s' % (domain, port)
            rm_state = self.redis.srem(entrypoints_key, e_id)
            base_key = '%s:%s:%s' % (EntrypointModel.__prefix_key__,
                                     balancer_name, e_id)
            if rm_state:
                self.redis.delete(base_key)
            return True
        return False

    def delete_all_entrypoint(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            entrypoints_key = '%s:%s' % (balancer_name,
                                         EntrypointModel.__prefix_key__)
            e_ids = self.redis.smembers(entrypoints_key)
            for e_id in e_ids:
                base_key = '%s:%s:%s' % (EntrypointModel.__prefix_key__,
                                         balancer_name, e_id)
                self.redis.delete(base_key)
            self.redis.delete(entrypoints_key)
            return True
        return False

    def get_nginx(self, nginx_name):
        if self.redis.sismember(NginxModel.__prefix_key__, nginx_name):
            nginx = NginxModel.create(
                name=nginx_name,
                upstream=self.get_upstream(nginx_name),
                server=self.get_server(nginx_name))
            return nginx

    def get_nginx_list(self):
        result = []
        nginx_names = self.redis.smembers(NginxModel.__prefix_key__)
        for nginx_name in nginx_names:
            nginx = self.get_nginx(nginx_name)
            result.append(nginx)
        return result

    def get_upstream(self, nginx_name):
        if self.redis.sismember(NginxModel.__prefix_key__, nginx_name):
            base_key = '%s:%s' % (UpstreamModel.__prefix_key__, nginx_name)
            mapping = self.redis.hgetall(base_key)
            mapping['servers'] = eval(mapping['servers'])
            upstream = UpstreamModel.create(**mapping)
            return upstream

    def update_upstream(self, upstream, nginx_name):
        if isinstance(upstream, dict) and upstream:
            base_key = '%s:%s' % (UpstreamModel.__prefix_key__, nginx_name)
            if 'name' in upstream.keys():
                upstream.pop('name')
            self.redis.hmset(base_key, upstream)
            return True
        return False

    def update_server(self, server, nginx_name):
        if isinstance(server, dict) and server:
            base_key = '%s:%s' % (ServerModel.__prefix_key__, nginx_name)
            if 'certificate' in server.keys():
                server['certificate'] = json.dumps(server['certificate'])
            self.redis.hmset(base_key, server)
            return True
        return False

    def get_server(self, nginx_name):
        if self.redis.sismember(NginxModel.__prefix_key__, nginx_name):
            base_key = '%s:%s' % (ServerModel.__prefix_key__, nginx_name)
            mapping = self.redis.hgetall(base_key)
            mapping['port'] = eval(mapping['port'])
            mapping['server_names'] = eval(mapping['server_names'])
            if 'certificate' in mapping.keys():
                mapping['certificate'] = json.loads(mapping['certificate'])
            server = ServerModel.create(**mapping)
            return server

    def save_nginx(self, nginx):
        if isinstance(nginx, dict) and nginx:
            self.redis.sadd(NginxModel.__prefix_key__, nginx.get('name'))
            self.save_upstream(nginx.get('upstream'), nginx.get('name'))
            self.save_server(nginx.get('server'), nginx.get('name'))
            return True

    def save_upstream(self, upstream, nginx_name):
        if self.redis.sismember(NginxModel.__prefix_key__, nginx_name):
            if not upstream and not isinstance(upstream, dict):
                upstream = {}
            base_key = '%s:%s' % (UpstreamModel.__prefix_key__, nginx_name)
            self.redis.hmset(base_key, upstream)
            return True

    def save_server(self, server, nginx_name):
        if self.redis.sismember(NginxModel.__prefix_key__, nginx_name):
            if not server and not isinstance(server, dict):
                server = {}
            base_key = '%s:%s' % (ServerModel.__prefix_key__, nginx_name)
            if 'certificate' in server.keys():
                server['certificate'] = json.dumps(server['certificate'])
            self.redis.hmset(base_key, server)
            return True

    def delete_nginx(self, nginx_name):
        if self.redis.sismember(NginxModel.__prefix_key__, nginx_name):
            self.delete_upstream(nginx_name)
            self.delete_server(nginx_name)
            self.redis.srem(NginxModel.__prefix_key__, nginx_name)
            return True
        return False

    def delete_upstream(self, nginx_name):
        if self.redis.sismember(NginxModel.__prefix_key__, nginx_name):
            base_key = '%s:%s' % (UpstreamModel.__prefix_key__, nginx_name)
            self.redis.delete(base_key)
            return True
        return False

    def delete_server(self, nginx_name):
        if self.redis.sismember(NginxModel.__prefix_key__, nginx_name):
            base_key = '%s:%s' % (ServerModel.__prefix_key__, nginx_name)
            self.redis.delete(base_key)
            return True
        return False
