# -*- coding: utf-8 -*-


import logging
import inspect
import socket
import struct

from inspect import (
    getmembers,
    ismethod
)

def autolog(message=None, level=logging.DEBUG):
    func = inspect.currentframe().f_back.f_code
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    logger = logging.getLogger(module.__name__)
    logger.log(level, '%s: %s' % (func.co_name, message))

def enum(**enums):
    return type('Enum', (), dict(enums.items() + {'items': enums}.items()))

def uberenum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    by_value = dict((value, key) for key, value in enums.iteritems())
    enums['by_value'] = by_value
    return type('Enum', (), enums)

def ip2long(ip):
    packed = socket.inet_aton(ip)
    return long(struct.unpack('!L', packed)[0])


def long2ip(lg):
    return socket.inet_ntoa(struct.pack('!L', lg))

def to_dict(o, limit=None):
    m = getmembers(o, lambda x: not ismethod(x))
    m = [i for i in m if not i[0].startswith('_')]
    if limit:
        m = [i for i in m if i[0] in limit]
    return dict(m)

_iterable_types = (
    tuple,
    list,
    set
)

class Circular(object):
    pass

def _is_collection(node):
    node_type = type(node)
    return node_type in _iterable_types or hasattr(node, '__iter__')

def _is_dict_like(node):
    node_type = type(node)
    return node_type in (dict,)

def _is_traversable(node):
    return hasattr(node, 'to_dict')

def _is_circular(node):
    return isinstance(node, Circular)

def to_dict_recursive(node, last_node=None, paths=None):
    if paths is None:
        paths = {}

    if _is_dict_like(node):
        new_dict = {}
        for key, value in node.iteritems():
            result = to_dict_recursive(value, last_node, paths)
            if _is_circular(result):
                continue
            new_dict[key] = result

        return new_dict

    if _is_collection(node):
        new_list = []

        for item in node:
            result = to_dict_recursive(item, last_node, paths)
            if _is_circular(result):
                continue
            new_list.append(result)

        return new_list

    if _is_traversable(node):
        node_id = id(node)
        last_node_id = None

        if last_node:
            last_node_id = id(last_node)

            if last_node_id in paths and node_id in paths[last_node_id]:
                return Circular()

            if node_id not in paths:
                paths[node_id] = ()

            paths[node_id] += (last_node_id,)

        node_dict = node.to_dict()
        return to_dict_recursive(node_dict, last_node=node, paths=paths)

    return node