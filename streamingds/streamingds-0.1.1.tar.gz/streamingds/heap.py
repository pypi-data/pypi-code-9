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
"""A collection of heap implementations with different storage backends.

The most simple one uses Pythons built in `heapq` in-memory module that can be
serialized using pickle.
"""
import heapq


class Heap(list):
    """A simple heap base class that defines a heap interface used by
    specialized implementations."""

    def min(self):
        """Return the heap's min element."""
        return self[0]

    def push(self, entry):
        heapq.heappush(self, entry)

    def pushpop(self, entry):
        return heapq.heappushpop(self, entry)

    def remove(self, entry):
        """This is O(2n) as list.remove is O(n) and heapq.heapify() as well."""
        if entry in self:
            super(Heap, self).remove(entry)
            heapq.heapify(self)
