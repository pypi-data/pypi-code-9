# -*- coding: UTF-8 -*-

"""
Constants for SyRPC
"""

# System imports

# Project imports


class General(object):
    """General constants"""
    APP_NAME    = 'syrpc'
    NUM_WORKERS = 2


class AMQ(object):
    """Constants for AMQ"""
    VIRTUALHOST = '/'
    TTL         = 3 * 60 * 60  # 3 hours
    MSG_TTL     = 10
    NUM_QUEUES  = 64
    HASH        = 'EdaeYa6eesh3ahSh'
    MSG_TYPE    = 'application/json'


class RPC(object):
    """Constants for RPC"""
    REQUEST_NAME = '{0}_request'
    RESULT_EXCHANGE_NAME = '{0}_result_exchange'
    RESULT_EXCHANGE_TYPE = 'direct'
    RESULT_QUEUE_NAME = '{0}_result_queue_{1}'
