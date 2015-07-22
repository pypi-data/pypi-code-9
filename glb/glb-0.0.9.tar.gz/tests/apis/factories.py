# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from factory import fuzzy, Sequence, SubFactory, Factory

from glb.models.balancer import Balancer
from glb.models.frontend import Frontend
from glb.models.entrypoint import Entrypoint
from glb.models.backend import Backend
from glb.models.slave import Slave
import datetime
import random

PROTOCOLS = ['http',
             'https',
             'tcp',
             'ssl']


class FrontendFactory(Factory):

    class Meta:
        model = Frontend

    port = random.randint(50000, 61000)
    protocol = fuzzy.FuzzyChoice(PROTOCOLS)


class EntrypointFactory(Factory):

    class Meta:
        model = Entrypoint

    domain = 'www.guokr.com'
    port = random.randint(1, 1024)
    protocol = 'https'
    cipher = '1234'
    certificate = {'private_key': '1234',
                   'public_key_certificate': '5678',
                   'certificate_chain': '9012'}


class BackendFactory(Factory):

    class Meta:
        model = Backend

    tag = Sequence(lambda n: "backend{0}".format(n))
    address = '%s.%s.%s.%s' % (
        random.randint(1, 254),
        random.randint(1, 254),
        random.randint(1, 254),
        random.randint(1, 254))
    port = random.randint(50000, 61000)


class BalancerFactory(Factory):

    class Meta:
        model = Balancer

    name = Sequence(lambda n: "balancer{0}".format(n))
    frontend = SubFactory(FrontendFactory)
    entrypoints = []
    backends = []


class SlaveFactory(Factory):

    class Meta:
        model = Slave

    address = '%s.%s.%s.%s' % (
        random.randint(1, 254),
        random.randint(1, 254),
        random.randint(1, 254),
        random.randint(1, 254))
    sync_time = str(datetime.datetime.now)
