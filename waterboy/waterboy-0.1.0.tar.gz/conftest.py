# -*- encoding: utf-8 -*-

import os
from datetime import datetime, date, time
from decimal import Decimal

import pytest

from waterboy import KVStore, RedisConfig
import waterboy.testing

MONGO_TEST_DATABASE = waterboy.testing.MONGO_TEST_DATABASE
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
MONGO_PORT = os.environ.get('MONGO_PORT', 27107)

@pytest.fixture
def defaults():
    return waterboy.testing.ConfigTestCase.DEFAULTS

@pytest.fixture
def redis(request, defaults):
    cfg = RedisConfig(initial=defaults)
    request.addfinalizer(cfg.clear)
    return cfg

@pytest.fixture
def mongo_test_database(request, scope='session'):
    MONGO_RUNNING = bool(int(os.environ.get('MONGO_RUNNING', 0)))
    if MONGO_RUNNING:
        from pymongo import MongoClient
        client = MongoClient(port=int(MONGO_PORT))
        db = client[MONGO_TEST_DATABASE]
        def dropdb():
            client.drop_database(MONGO_TEST_DATABASE)
            print("Dropped mongo database '%s'" % MONGO_TEST_DATABASE)
        request.addfinalizer(dropdb)
        return db

@pytest.fixture
def mongo(request, mongo_test_database, defaults):
    cfg = MongoConfig(MONGO_TEST_DATABASE, initial=defaults)
    request.addfinalizer(cfg.clear)
    return cfg

