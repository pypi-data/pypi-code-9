# -*- encoding: utf-8 -*-
import os
import pytest

import waterboy.testing

MONGO_TEST_DATABASE = waterboy.testing.MONGO_TEST_DATABASE

REDIS_RUNNING = bool(int(os.environ.get('REDIS_RUNNING', 0)))
MONGO_RUNNING = bool(int(os.environ.get('MONGO_RUNNING', 0)))
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
MONGO_PORT = os.environ.get('MONGO_PORT', 27107)

class TestDictConfig(waterboy.testing.ConfigTestCase):
    """Test the dummy 'dict' backend."""

    BACKEND = 'dict'

###############################################################################
# Redis Tests                                                                 #
###############################################################################
def skipifnoredis(*args, **kwargs):
    return pytest.mark.skipif(not REDIS_RUNNING, reason='No redis server found.')(*args, **kwargs)

@skipifnoredis
def test_server_ping(redis):
    assert redis.backend.client.ping() is True

@skipifnoredis
class TestRedisConfig(waterboy.testing.ConfigTestCase):
    """Test the redis backend."""

    BACKEND = 'redis'

###############################################################################
# MongoDB Tests                                                               #
###############################################################################
def skipifnomongo(*args, **kwargs):
    return pytest.mark.skipif(not MONGO_RUNNING, reason='No mongodb server found.')(*args, **kwargs)

if MONGO_RUNNING:
    @pytest.mark.usefixtures("mongo_test_database")
    class TestMongoConfig(waterboy.testing.ConfigTestCase):
        """Test the mongo backend."""

        BACKEND = 'mongo'
        BACKEND_PARAMS = [MONGO_TEST_DATABASE]

