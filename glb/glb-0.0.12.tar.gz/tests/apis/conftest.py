# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import os

import pytest
from webtest import TestApp
from glb.command import create_app
from glb.core.extensions import (db as _db,
                                 redis as _redis)
from .factories import (FrontendFactory,
                        EntrypointFactory,
                        BackendFactory,
                        BalancerFactory,
                        SlaveFactory)


def pytest_runtest_setup(item):
    os.environ['DEBUG'] = '1'
    os.environ['TESTING'] = '1'
    os.environ['LOGIN_DISABLED'] = '1'
    os.environ['REDIS_HOST'] = 'localhost'
    os.environ['REDIS_PORT'] = '6379'
    os.environ['REDIS_DB'] = '14'


@pytest.yield_fixture(scope='session')
def app():
    _app = create_app(dict(
        REDIS_DB=14,
        DEBUG=True))
    ctx = _app.test_request_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.fixture(scope='session')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope='session')
def db(app):
    yield _db
    _redis.flushdb()


@pytest.fixture(scope='function')
def balancer(db):
    balancer = BalancerFactory.get_bean()
    db.save_balancer(balancer)
    return balancer

@pytest.fixture(scope='function')
def slave(db):
    slave = SlaveFactory.get_bean()
    db.save_slave(slave)
    return slave
