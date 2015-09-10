# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import os.path
from collections import OrderedDict
from six import string_types
from igor.jsutil import json_dumps, json_loads
from ..core import ensure_dirs


class CachedObj(OrderedDict):
    def __init__(self, *args, **kw):
        self._cache_path = None
        if len(args) == 1 and isinstance(args[0], string_types):
            for key, value in json_loads(args[0], CachedObj).items():
                self[key] = value
        else:
            super(CachedObj, self).__init__(*args, **kw)

    @classmethod
    def load_file(self, path):
        ensure_dirs(path)
        ret = None
        if os.path.exists(path):
            with open(path) as fp:
                json = fp.read() or '{}'
                ret = json_loads(json, CachedObj)
        else:
            ret = CachedObj()

        ret._set_cache_path(path)
        return ret

    def reset(self):
        for key in self:
            del self[key]
        if os.path.exists(self._cache_path):
            os.remove(self._cache_path)

    def _set_cache_path(self, path):
        self._cache_path = path
        if len(self) > 0:
            self._save_changes()

    def _save_changes(self):
        if self._cache_path is not None:
            with open(self._cache_path, 'w') as fp:
                fp.write(json_dumps(self))

    def members(self):
        return dict(self.items())

    def __repr__(self):
        return '<{0}>'.format(str(dict(self)))

    def __str__(self, indent = None):
        """ Use JSON as string representation """
        return str(self.__unicode__(indent))

    def __unicode__(self, indent = None):
        return json_dumps(self, indent=indent)

    def __setattr__(self, name, value):
        try:
            if name in ('_cache_path',) or name.startswith('_'):
                super(CachedObj, self).__setattr__(name, value)
            else:
                self[name] = value
                self._save_changes()
        except:
            import ipdb; ipdb.set_trace()

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("No attribute {}".format(name))

