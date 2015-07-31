#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
Encoder-Decoder
"""
__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


import collections

try:
    import json
except ImportError:
    from django.utils import simplejson as json


class JSONDecoder(json.JSONDecoder):
    """
    Ordered Decoder
    """

    def __init__(self, *args, **kwargs):
        super(JSONDecoder, self).__init__(
            object_pairs_hook=collections.OrderedDict, *args, **kwargs)


def total_seconds(timedelta):
    # TimeDelta.total_seconds() is only available in Python 2.7
    if hasattr(timedelta, 'total_seconds'):
        return timedelta.total_seconds()
    else:
        return ((timedelta.days * 86400.0) + float(timedelta.seconds) +
                (timedelta.microseconds / 1000000.0))


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if hasattr(obj, '__getitem__'):
            try:
                return dict(obj)
            except:
                pass
        if hasattr(obj, '__iter__'):
            return tuple(item for item in obj)
        return super(JSONEncoder, self).default(obj)


def decode(value):
    return json.loads(value, cls=JSONDecoder)


def encode(value):
    return json.dumps(value, cls=JSONEncoder)
