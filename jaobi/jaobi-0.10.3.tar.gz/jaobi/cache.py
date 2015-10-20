# -*- coding: utf-8 -*-

from copy import copy
from pyrocumulus.conf import settings
from tornado import gen
from jaobi.models import ContentConsumption


class _SizedConsumptionCache:

    def __init__(self):
        self.cache = []
        self.cache_size = settings.CONSUMPTION_CACHE_SIZE

    @gen.coroutine
    def add(self, obj):
        self.cache.append(obj)
        if len(self.cache) >= self.cache_size:
            to_insert = copy(self.cache)
            self.cache = []
            yield self.insert(to_insert)

    @gen.coroutine
    def insert(self, obj_list):
        yield ContentConsumption.objects.insert(obj_list)


sized_cache = _SizedConsumptionCache()


def get_cache(cache_type='sized'):
    return sized_cache
