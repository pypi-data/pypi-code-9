# -*- coding: utf-8 -*-
'''
LMDB database store.

shove's URI for LMDB stores follows the form:

lmdb://<path>

Where <path> is a URL path to a LMDB database. Alternatively, the native
pathname to a LMDB database can be passed as the 'engine' parameter.
'''
from stuf.six import b, tounicode, PY3

from shove.store import ClientStore


try:
    import lmdb
except ImportError:
    raise ImportError('requires lmdb library')


__all__ = ['LMDBStore']


class LMDBStore(ClientStore):

    '''
    LMDB-based object storage frontend.
    '''

    init = 'lmdb://'

    def __init__(self, engine, **kw):
        super(LMDBStore, self).__init__(engine, **kw)
        self._store = lmdb.open(self._engine)

    def __getitem__(self, key):
        with self._store.begin() as tx:
            value = tx.get(b(key))
            if value is not None:
                item = self.loads(value)
                if item is not None:
                    return item
                raise KeyError(key)
            raise KeyError(key)

    def __setitem__(self, key, value):
        with self._store.begin(write=True) as tx:
            tx.put(b(key), self.dumps(value))

    def __delitem__(self, key):
        with self._store.begin(write=True) as tx:
            tx.delete(b(key))

    def __len__(self):
        return self._store.stat()['entries']

    def __iter__(self):
        with self._store.begin() as tx:
            cursor = tx.cursor()
            cursor.first()
            for key in cursor.iternext_nodup(True, False):
                yield tounicode(key) if PY3 else key