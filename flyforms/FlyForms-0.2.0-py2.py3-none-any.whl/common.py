# coding=utf-8
from collections import Iterable, Mapping

from flyforms.compatibility import string_types


UNSET = object()  # the default mark for not set values

is_set = lambda value: value is not UNSET

# Supported types for JSON encoding and decoding operations
jsonify_types = (bool, int, float, Iterable, Mapping) + string_types


class FrozenDict(Mapping):
    """
    Immutable dictionary implementation
    stolen from StackOverflow_

    .. _StackOverflow: http://stackoverflow.com/questions/2703599/what-would-a-frozen-dict-be
    """

    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)
        self._hash = None

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __hash__(self):
        if self._hash is None:
            self._hash = 0
            for pair in self.iteritems():
                self._hash ^= hash(pair)
        return self._hash
