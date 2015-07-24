# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from glb.settings import Config
from glb.models.balancer import Balancer as BalancerModel
from glb.models.frontend import Frontend as FrontendModel
from glb.models.backend import Backend as BackendModel
from glb.models.slave import Slave as SlaveModel
from glb.models.entrypoint import Entrypoint as EntrypointModel


class DB(object):

    def __init__(self, redis):
        self.redis = redis

    def _get_class_members(self, cls):
        return cls().as_dict().keys()

    def get_balancer(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            balancer = BalancerModel(balancer_name)
            balancer.frontend = self.get_frontend(balancer_name)
            balancer.backends = self.get_backend_list(balancer_name)
            balancer.entrypoints = self.get_entrypoint_list(balancer_name)
            return balancer

    def get_frontend(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            frontend = FrontendModel()
            for k in self._get_class_members(FrontendModel):
                setattr(frontend, k, self.redis.get('%s:%s:%s' % (
                    FrontendModel.__prefix_key__, balancer_name, k)))
            return frontend

    def get_slave(self, address):
        if self.redis.sismember(SlaveModel.__prefix_key__, address):
            slave = SlaveModel(address=address)
            for k in self._get_class_members(SlaveModel):
                if k != 'address':
                    setattr(slave, k, self.redis.get(
                        '%s:%s:%s' % (SlaveModel.__prefix_key__, address, k)))
            return slave

    def get_balancer_list(self):
        result = []
        b_names = self.redis.smembers(BalancerModel.__prefix_key__)
        for b_name in b_names:
            balancer = self.get_balancer(b_name)
            result.append(balancer)
        return result

    def get_backend_list(self, balancer_name):
        result = []
        backends_key = '%s:%s' % (balancer_name, BackendModel.__prefix_key__)
        b_ids = self.redis.smembers(backends_key)
        for b_id in b_ids:
            backend = BackendModel()
            addr_port = b_id.split(':')
            setattr(backend, 'address', addr_port[0])
            setattr(backend, 'port', int(addr_port[1]))
            base_key = '%s:%s:%s' % (
                BackendModel.__prefix_key__, balancer_name, b_id)
            for k in self._get_class_members(BackendModel):
                if k != 'address' and k != 'port':
                    setattr(backend, k,
                            self.redis.get('%s:%s' % (base_key, k)))
            result.append(backend)
        return result

    def get_entrypoint_list(self, balancer_name):
        result = []
        entrypoints_key = '%s:%s' % (
            balancer_name, EntrypointModel.__prefix_key__)
        e_ids = self.redis.smembers(entrypoints_key)
        for e_id in e_ids:
            entrypoint = EntrypointModel()
            base_key = '%s:%s:%s' % (
                EntrypointModel.__prefix_key__, balancer_name, e_id)
            domain_port = e_id.split(':')
            setattr(entrypoint, 'domain', domain_port[0])
            setattr(entrypoint, 'port', int(domain_port[1]))
            for k in self._get_class_members(EntrypointModel):
                if k != 'domain' and k != 'port':
                    v = self.redis.get('%s:%s' % (base_key, k))
                    if k == 'certificate' and v:
                        v = eval(v)
                    setattr(entrypoint, k, v)
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
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return balancer

    def save_frontend(self, frontend, balancer_name):
        if isinstance(frontend, FrontendModel) and self.redis.sismember(
                BalancerModel.__prefix_key__, balancer_name):
            for k, v in frontend.as_dict().items():
                if k == 'port':
                    self.redis.watch(Config.PORTS_NUMBER_COUNT_KEY)
                    v = int(self.redis.get(Config.PORTS_NUMBER_COUNT_KEY))
                    if v > Config.PORT_RANGE[0]:
                        p = self.redis.pipeline()
                        p.decr(Config.PORTS_NUMBER_COUNT_KEY)
                        p.execute()
                self.redis.set(('%s:%s:%s' % (
                    frontend.__prefix_key__, balancer_name, k)), v)
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return frontend

    def update_frontend(self, frontend, balancer_name):
        if isinstance(frontend, FrontendModel) and self.redis.sismember(
                BalancerModel.__prefix_key__, balancer_name):
            for k, v in frontend.as_dict().items():
                if k != 'port' and v:
                    self.redis.set(('%s:%s:%s' % (
                        frontend.__prefix_key__, balancer_name, k)), v)
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return True
        return False

    def save_or_update_backend(self, backend, balancer_name):
        ''' use backend address and port as id '''
        if isinstance(backend, BackendModel) and self.redis.sismember(
                BalancerModel.__prefix_key__, balancer_name):
            backend_id = '%s:%s' % (backend.address, backend.port)
            for k, v in backend.as_dict().items():
                if k != 'address' and k != 'port' and v:
                    self.redis.set(('%s:%s:%s:%s' % (
                        backend.__prefix_key__, balancer_name,
                        backend_id, k)), v)
                backends_key = '%s:%s' % (
                    balancer_name, backend.__prefix_key__)
                self.redis.sadd(backends_key, backend_id)
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return backend

    def save_or_update_entrypoint(self, entrypoint, balancer_name):
        if isinstance(entrypoint, EntrypointModel) and self.redis.sismember(
                BalancerModel.__prefix_key__, balancer_name):
            entrypoint_key = '%s:%s' % (
                balancer_name, entrypoint.__prefix_key__)
            for k, v in entrypoint.as_dict().items():
                if k != 'domain' and k != 'port' and v:
                    e_id = '%s:%s' % (entrypoint.domain, entrypoint.port)
                    self.redis.set(('%s:%s:%s:%s' % (
                        entrypoint.__prefix_key__, balancer_name, e_id, k)), v)
                    self.redis.sadd(entrypoint_key, e_id)
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return entrypoint

    def save_slave(self, slave):
        if isinstance(slave, SlaveModel):
            self.redis.sadd(slave.__prefix_key__, slave.address)
            for k, v in slave.as_dict().items():
                if k != 'address':
                    self.redis.set(('%s:%s:%s' % (
                        slave.__prefix_key__, slave.address, k)), v)
        return slave

    def delete_balancer(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            self.delete_frontend(balancer_name)
            self.delete_all_backend(balancer_name)
            self.delete_all_entrypoint(balancer_name)
            self.redis.srem(BalancerModel.__prefix_key__, balancer_name)
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return True
        return False

    def _delete_end(self, cls, base_key):
        for k in self._get_class_members(cls):
            self.redis.delete('%s:%s' % (base_key, k))

    def delete_frontend(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            self._delete_end(FrontendModel, '%s:%s' % (
                FrontendModel.__prefix_key__, balancer_name))
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return True
        return False

    def delete_backend(self, balancer_name, address, port):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            backends_key = '%s:%s' % (
                balancer_name, BackendModel.__prefix_key__)
            b_id = '%s:%s' % (address, port)
            rm_state = self.redis.srem(backends_key, b_id)
            base_key = '%s:%s:%s' % (
                BackendModel.__prefix_key__, balancer_name, b_id)
            if rm_state:
                self._delete_end(BackendModel, base_key)
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return True
        return False

    def delete_backend_by_tag(self, balancer_name, tag):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            backends_key = '%s:%s' % (
                balancer_name, BackendModel.__prefix_key__)
            b_ids = self.redis.smembers(backends_key)
            base_key = '%s:%s' % (BackendModel.__prefix_key__, balancer_name)
            for b_id in b_ids:
                r_tag = self.redis.get('%s:%s:%s' % (base_key, b_id, 'tag'))
                if r_tag == tag:
                    self._delete_end(BackendModel, '%s:%s' % (base_key, b_id))
                    self.redis.srem(backends_key, b_id)
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return True
        return False

    def delete_all_backend(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            backends_key = '%s:%s' % (
                balancer_name, BackendModel.__prefix_key__)
            base_keys = self.redis.smembers(backends_key)
            for base_key in base_keys:
                self._delete_end(BackendModel, '%s:%s:%s' % (
                    BackendModel.__prefix_key__, balancer_name, base_key))
            self.redis.delete(backends_key)
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return True
        return False

    def delete_entrypoint(self, balancer_name, domain, port):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            entrypoints_key = '%s:%s' % (
                balancer_name, EntrypointModel.__prefix_key__)
            e_id = '%s:%s' % (domain, port)
            rm_state = self.redis.srem(entrypoints_key, e_id)
            base_key = '%s:%s:%s' % (
                EntrypointModel.__prefix_key__, balancer_name, e_id)
            if rm_state:
                self._delete_end(EntrypointModel, base_key)
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return True
        return False

    def delete_all_entrypoint(self, balancer_name):
        if self.redis.sismember(BalancerModel.__prefix_key__, balancer_name):
            entrypoints_key = '%s:%s' % (
                balancer_name, EntrypointModel.__prefix_key__)
            base_keys = self.redis.smembers(entrypoints_key)
            for base_key in base_keys:
                self._delete_end(EntrypointModel, '%s:%s:%s' % (
                    EntrypointModel.__prefix_key__, balancer_name, base_key))
            self.redis.delete(entrypoints_key)
            latest_version = str(datetime.datetime.now)
            self.redis.publish(Config.LISTEN_REDIS_CHANNEL,  latest_version)
            self.redis.set(Config.LATEST_VERSION, latest_version)
            return True
        return False
