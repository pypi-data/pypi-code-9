# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2013 Daniel Truemper <truemped at googlemail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
from __future__ import (absolute_import, division, print_function,
                        with_statement)

from streamingds.bloomfilter import BloomFilter
from streamingds.redis.hashing import RedisHashing


class RedisBloomFilter(RedisHashing, BloomFilter):
    """Version of the bloomfilter that persists stuff in redis."""

    def __init__(self, capacity, error_rate=0.001, redis_host='localhost',
                 redis_port=6379, redis_prefix='bloomfilter'):

        RedisHashing.__init__(self, redis_host, redis_port, redis_prefix)
        BloomFilter.__init__(self, capacity, error_rate)

    @property
    def bitarray(self):
        if not hasattr(self, '_bitarray'):
            self._bitarray = RedisBitArray(self.redis,
                                           self._redis_key('bitarray'),
                                           self.slices)
        return self._bitarray


class RedisBitArray(object):
    """Simple mapper for bitarray methods to redis commands."""

    def __init__(self, redis, key, slices):
        self._redis = redis
        self._key = key

        if self._redis.strlen(key) == 0:
            s = int(slices / 8)
            if slices % 8 > 0:
                s += 1
            self._redis.set(key, '\0' * s)

    def set(self, value, bits):
        for bit in bits:
            self._redis.setbit(self._key, bit, value)

    def all(self, value, bits):
        return all([self._redis.getbit(self._key, bit) for bit in bits])

    def count(self, value):
        return self._redis.bitcount(self._key)
