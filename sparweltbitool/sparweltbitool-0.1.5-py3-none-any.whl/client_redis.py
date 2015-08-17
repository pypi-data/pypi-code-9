import redis

from sparweltbitool.config import config
from sparweltbitool.singleton import Singleton


@Singleton
class ClientRedis(object):
    """ Operations with Redis."""

    def __init__(self):

        self.r = redis.StrictRedis(
            host=config.get('redis', 'host'),
            port=config.get('redis', 'port'),
            db=config.get('redis', 'db'))
