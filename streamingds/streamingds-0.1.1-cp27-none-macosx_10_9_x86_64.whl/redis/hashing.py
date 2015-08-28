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

import random

from streamingds.hashing import Hashing
from streamingds.redis.base import BaseRedis


class RedisHashing(BaseRedis, Hashing):
    """Base class that stores all necessary data for hashing in redis."""

    def __init__(self, redis_host, redis_port, redis_prefix):
        BaseRedis.__init__(self, redis_host, redis_port, redis_prefix)

    @property
    def bits_per_slice(self):
        return int(self.redis.get(self._redis_key('bits_per_slice')))

    @bits_per_slice.setter
    def bits_per_slice(self, value):
        self.redis.set(self._redis_key('bits_per_slice'), value)

    @property
    def slices(self):
        return int(self.redis.get(self._redis_key('slices')))

    @slices.setter
    def slices(self, value):
        self.redis.set(self._redis_key('slices'), value)

    @property
    def seeds(self):
        k = self._redis_key('seeds')
        l = self.redis.llen(k)
        if l == 0:
            s = [random.randint(0, 2 ** 32)
                 for _ in range(self.bits_per_slice)]
            self.redis.lpush(k, *s)
        return [int(seed) for seed in self.redis.lrange(k, 0, l)]
