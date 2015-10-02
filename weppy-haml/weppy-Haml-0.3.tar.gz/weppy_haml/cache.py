# -*- coding: utf-8 -*-
"""
    weppy_haml.cache
    ----------------

    Cache for Haml templates

    :copyright: (c) 2015 by Giovanni Barillari
    :license: BSD, see LICENSE for more details.
"""

from weppy._compat import PY2, hashlib_md5, to_bytes


def make_md5(value):
    if PY2:
        value = to_bytes(value)
    return hashlib_md5(value).hexdigest()[:8]


class HamlCache(object):
    data = {}
    hashes = {}

    def get(self, filename, source):
        hashed = make_md5(source)
        if self.hashes.get(filename) != hashed:
            return None
        return self.data.get(filename)

    def set(self, filename, source, compiled):
        self.data[filename] = compiled
        self.hashes[filename] = make_md5(source)
