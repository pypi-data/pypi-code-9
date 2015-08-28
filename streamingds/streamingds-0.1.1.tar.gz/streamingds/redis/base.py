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

try:
    from redis import StrictRedis
except ImportError:
    print('Cannot import redis. Not using persistance.')
    raise


class BaseRedis(object):
    """Base class for dealing with redis communication."""

    def __init__(self, redis_host, redis_port, redis_prefix):
        self._redis_host = redis_host
        self._redis_port = redis_port
        self._redis_prefix = redis_prefix

    @property
    def redis(self):
        """Return a `StrictRedis` instance."""
        if not hasattr(self, '_redis'):
            self._redis = StrictRedis(self._redis_host, self._redis_port)
        return self._redis

    def _redis_key(self, key):
        """Return the computed redis key for the internal key.

        If the `redis_prefix` was *bloomfilter* the `RedisBloomFilter` will
        create keys like *bloomfilter:bitarray*.
        """
        return ':'.join([self._redis_prefix, key])


class RedisTwoDimensionalArray(object):

    def __init__(self, redis, prefix, slices, bits_per_slice):
        self._lists = []

        slice_key = '%s:slices' % prefix
        if redis.exists(slice_key) and slices != int(redis.get(slice_key)):
            raise ValueError(
                'Sketch already exists with different configuration')

        bits_p_s_key = '%s:bits_per_slice' % prefix
        if (redis.exists(bits_p_s_key) and
                bits_per_slice != int(redis.get(bits_p_s_key))):
            raise ValueError(
                'Sketch already exists with a different configuration')

        for i in range(bits_per_slice):
            self._lists.append(RedisList(redis, ':'.join([prefix, str(i)]),
                                         slices))

    def __getitem__(self, idx):
        return self._lists[idx]


class RedisList(object):

    def __init__(self, redis, prefix, length):
        self._redis = redis
        self._prefix = prefix

        if not self._redis.exists(prefix):
            for _ in range(length):
                self._redis.lpush(prefix, 0)

    def __getitem__(self, idx):
        return int(self._redis.lrange(self._prefix, idx, idx)[0])

    def __setitem__(self, idx, value):
        self._redis.lset(self._prefix, idx, value)
