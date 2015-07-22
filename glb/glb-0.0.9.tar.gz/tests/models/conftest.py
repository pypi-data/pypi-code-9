# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import pytest
import datetime
import redis as _redis
from glb.core.db import DB
from glb.settings import Config
from .factories import (FrontendFactory,
                        EntrypointFactory,
                        BackendFactory,
                        BalancerFactory,
                        SlaveFactory)


@pytest.yield_fixture(scope='session')
def redis():
    redis = _redis.StrictRedis.from_url("redis://localhost:6379/11")
    if not redis.exists(Config.PORTS_NUMBER_COUNT_KEY):
        ''' init current port value can be assigned '''
        redis.set(Config.PORTS_NUMBER_COUNT_KEY, Config.PORT_RANGE[1])
    if not redis.exists(Config.LATEST_VERSION):
        redis.set(Config.LATEST_VERSION, str(datetime.datetime.now()))
    yield redis
    redis.flushdb()


@pytest.fixture(scope='session')
def db(redis):
    return DB(redis)

@pytest.fixture
def balancer(db):
    balancer = BalancerFactory()
    backend = BackendFactory()
    balancer.backends.append(backend)
    entrypoint = EntrypointFactory()
    balancer.entrypoints.append(entrypoint)
    db.save_balancer(balancer)
    return balancer

@pytest.fixture
def slave(db):
    slave = SlaveFactory()
    db.save_slave(slave)
    return slave
