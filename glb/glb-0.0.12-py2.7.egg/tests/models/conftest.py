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
    yield redis


@pytest.fixture(scope='session')
def db(redis):
    db = DB(redis)
    db.init_redis()
    return db

@pytest.fixture
def balancer(db):
    balancer = BalancerFactory.get_bean()
    db.save_balancer(balancer)
    return balancer

@pytest.fixture
def slave(db):
    slave = SlaveFactory.get_bean()
    db.save_slave(slave)
    return slave
