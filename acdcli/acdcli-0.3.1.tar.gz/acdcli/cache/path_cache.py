import os
from .db import NodeCache


class PathCache(NodeCache):
    def __init__(self, cache):
        self.cache = cache
        self.paths = {}
        self._add(cache.get_root_node())

    def __getattr__(self, item):
        return getattr(self.cache, item)

    def _add(self, node, basedir: str = ''):
        if not node.is_available():
            return

        self.paths[os.path.join(basedir, node.name if node.name else '/')] = node

        if node.is_folder():
            for c in node.available_children():
                self._add(c, os.path.join(basedir, node.simple_name()))

    def resolve(self, path: str, trash=False):
        if trash:
            return self.cache.resolve(path, trash=True)
        try:
            n = self.paths[path]
            ppath = os.path.dirname(path)
            p = self.paths[ppath] if ppath != '/' else None
            return n, p
        except KeyError:
            return self.cache.resolve(path)
