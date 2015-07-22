#! -*- coding: utf-8 -*-

#import redis

#from glb.settings import Config

#REDIS_URL = Config.REDIS_URL
#print REDIS_URL
#redis = redis.StrictRedis.from_url(REDIS_URL)

#if not redis.exists(Config.PORTS_NUMBER_COUNT_KEY):
#    ''' init current port value can be assigned '''
#    redis.set(Config.PORTS_NUMBER_COUNT_KEY, Config.PORT_RANGE[1])
