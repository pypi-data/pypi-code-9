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

from streamingds.countminsketch import CountMinSketch
from streamingds.redis.base import RedisTwoDimensionalArray
from streamingds.redis.hashing import RedisHashing


class RedisCountMinSketch(RedisHashing, CountMinSketch):
    """Redis backed count-min sketch"""

    def __init__(self, delta, epsilon, k, redis_host='localhost',
                 redis_port=6379, redis_prefix='countminsketch'):
        RedisHashing.__init__(self, redis_host, redis_port, redis_prefix)
        CountMinSketch.__init__(self, delta, epsilon, k)

    @property
    def count(self):
        """A wrapper around the internal 2-dimensional array storing the
        values for the `Count-Min Sketch`.
        """
        if not hasattr(self, '_count'):
            self._count = RedisTwoDimensionalArray(self.redis,
                                                   self._redis_prefix,
                                                   self.slices,
                                                   self.bits_per_slice)
        return self._count
