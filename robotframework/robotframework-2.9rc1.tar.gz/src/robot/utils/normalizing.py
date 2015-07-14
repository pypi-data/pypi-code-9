#  Copyright 2008-2015 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re
import sys
from collections import MutableMapping

from .robottypes import is_dict_like


_WHITESPACE_REGEXP = re.compile('\s+')


def normalize(string, ignore=(), caseless=True, spaceless=True):
    """Normalizes given string according to given spec.

    By default string is turned to lower case and all whitespace is removed.
    Additional characters can be removed by giving them in `ignore` list.
    """
    if spaceless:
        string = _WHITESPACE_REGEXP.sub('', string)
    if caseless:
        string = lower(string)
        ignore = [lower(i) for i in ignore]
    for ign in ignore:
        if ign in string:  # performance optimization
            string = string.replace(ign, '')
    return string


# http://ironpython.codeplex.com/workitem/33133
if sys.platform == 'cli' and sys.version_info < (2, 7, 5):
    def lower(string):
        return ('A' + string).lower()[1:]
else:
    def lower(string):
        return string.lower()


class NormalizedDict(MutableMapping):
    """Custom dictionary implementation automatically normalizing keys."""

    def __init__(self, initial=None, ignore=(), caseless=True, spaceless=True):
        """Initializes with possible initial value and normalizing spec.

        Initial values can be either a dictionary or an iterable of name/value
        pairs. In the latter case items are added in the given order.

        Normalizing spec has exact same semantics as with `normalize` method.
        """
        self._data = {}
        self._keys = {}
        self._normalize = lambda s: normalize(s, ignore, caseless, spaceless)
        if initial:
            self._add_initial(initial)

    def _add_initial(self, initial):
        items = initial.items() if hasattr(initial, 'items') else initial
        for key, value in items:
            self[key] = value

    def __getitem__(self, key):
        return self._data[self._normalize(key)]

    def __setitem__(self, key, value):
        norm_key = self._normalize(key)
        self._data[norm_key] = value
        self._keys.setdefault(norm_key, key)

    def __delitem__(self, key):
        norm_key = self._normalize(key)
        del self._data[norm_key]
        del self._keys[norm_key]

    def __iter__(self):
        return (self._keys[norm_key] for norm_key in sorted(self._keys))

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(dict(self.items()))

    def __eq__(self, other):
        if not is_dict_like(other):
            return False
        if not isinstance(other, NormalizedDict):
            other = NormalizedDict(other)
        return self._data == other._data

    def copy(self):
        copy = NormalizedDict()
        copy._data = self._data.copy()
        copy._keys = self._keys.copy()
        copy._normalize = self._normalize
        return copy

    def clear(self):
        # Faster than default implementation of MutableMapping.clear
        self._data.clear()
        self._keys.clear()
