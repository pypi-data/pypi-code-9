# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import datetime
from glb.models.balancer import Balancer
from glb.models.frontend import Frontend
from glb.models.entrypoint import Entrypoint
from glb.models.backend import Backend
from glb.models.slave import Slave

PROTOCOLS = ('http', 'https', 'tcp', 'ssl')
DOMAIN = ('www.guokr.com', 'www.zaih.com',
          'www.sex.guokr.com', 'www.mooc.guokr.com')


class FrontendFactory(object):

    @classmethod
    def get_bean(cls):
        port = random.randint(50000, 61000)
        protocol = random.choice(PROTOCOLS)
        return Frontend.create(port=port, protocol=protocol)


class EntrypointFactory(object):

    @classmethod
    def get_bean(cls):
        domain = random.choice(DOMAIN)
        port = random.randint(1, 1024)
        protocol = random.choice(PROTOCOLS)
        data = dict(domain=domain, port=port, protocol=protocol)
        if protocol == 'https':
            data['cipher'] = '1234'
            data['certificate'] = {'private_key': '1234',
                                   'public_key_certificate': '5678',
                                   'certificate_chain': '9012'}
        return Entrypoint.create(**data)


class BackendFactory(object):

    @classmethod
    def get_bean(cls):
        tag = 'version_test'
        address = '%s.%s.%s.%s' % (
            random.randint(1, 254),
            random.randint(1, 254),
            random.randint(1, 254),
            random.randint(1, 254))
        port = random.randint(50000, 61000)
        return Backend.create(address=address, port=port, tag=tag)


class BalancerFactory(object):

    @classmethod
    def get_bean(cls):
        name = 'balancer%s' % random.randint(1, 10000)
        frontend = FrontendFactory.get_bean()
        entrypoints = [EntrypointFactory.get_bean()
                       for i in xrange(random.randint(1, 4))]
        backends = [BackendFactory.get_bean()
                    for i in xrange(random.randint(1, 4))]
        return Balancer.create(name=name,
                               frontend=frontend,
                               entrypoints=entrypoints,
                               backends=backends)


class SlaveFactory(object):

    @classmethod
    def get_bean(cls):
        address = '%s.%s.%s.%s' % (
            random.randint(1, 254),
            random.randint(1, 254),
            random.randint(1, 254),
            random.randint(1, 254))
        sync_time = str(datetime.datetime.now())
        return Slave.create(address=address, sync_time=sync_time)
