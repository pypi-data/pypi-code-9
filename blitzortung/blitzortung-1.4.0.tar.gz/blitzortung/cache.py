# -*- coding: utf8 -*-

"""
Copyright (C) 2013 Andreas Würl

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

from __future__ import division
import time


class CacheEntry(object):
    def __init__(self, payload, expiry_time):
        self.__payload = payload
        self.__expiry_time = expiry_time
        self.__hit_count = 0

    def is_valid(self, current_time):
        return current_time < self.__expiry_time

    def get_payload(self):
        self.__hit_count += 1
        return self.__payload

    def get_hit_count(self):
        return self.__hit_count


class ObjectCache(object):

    __KWA_MARK = object()

    def __init__(self, ttl_seconds=30):
        self.__ttl_seconds = int(ttl_seconds)
        self.total_count = 0
        self.total_hit_count = 0

        self.cache = {}

    def get(self, cached_object_creator, *args, **kwargs):
        self.total_count += 1

        cache_key = (cached_object_creator,) + args + (ObjectCache.__KWA_MARK,) + tuple(sorted(kwargs.items()))
        current_time = int(time.time())

        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if entry.is_valid(current_time):
                self.total_hit_count += 1
                return entry.get_payload()

        expires = current_time + self.__ttl_seconds
        payload = cached_object_creator(*args, **kwargs)

        entry = CacheEntry(payload, expires)
        self.cache[cache_key] = entry

        return entry.get_payload()

    def clear(self):
        self.total_count = 0
        self.total_hit_count = 0
        self.cache.clear()

    def get_time_to_live(self):
        return self.__ttl_seconds

    def get_ratio(self):
        if self.total_hit_count == 0:
            return 0.0
        return self.total_hit_count / self.total_count