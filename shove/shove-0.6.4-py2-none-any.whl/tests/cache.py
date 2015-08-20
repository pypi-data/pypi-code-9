# class DBStore(ClientStore):
#
#     '''
#     sqlite-based object storage frontend.
#     '''
#
#     init = 'db://'
#
#     def __init__(self, engine, **kw):
#         super(DBStore, self).__init__(engine, **kw)
#         # make store table
#         self._store = sqlite3.connect(self._engine)
#         self._store.text_factory = native
#         self._cursor = self._store.cursor()
#         # create store table if it does not exist
#         self._cursor.execute(
#             '''
#             CREATE TABLE IF NOT EXISTS shove (
#                 key VARCHAR(255) PRIMARY KEY NOT NULL,
#                 value TEXT NOT NULL
#             )
#             '''
#         )
#         self._store.commit()
#
#     def __getitem__(self, key):
#         self._cursor.execute(
#             'SELECT value FROM shove WHERE key=?', (key,)
#         )
#         row = self._cursor.fetchone()
#         if row is not None:
#             return self.loads(native(row))
#         raise KeyError(key)
#
#     def __setitem__(self, k, v):
#         # update database if key already present
#         if k in self:
#             self._cursor.execute(
#                 'UPDATE shove SET value=? WHERE key=?', (self.dumps(v), k)
#             )
#         # insert new key if key not present
#         else:
#             self._cursor.execute('INSERT INTO shove VALUES (?, ?)', (k, self.dumps(v)))
#         self._store.commit()
#
#     def __delitem__(self, key):
#         self._cursor.execute('DELETE FROM shove WHERE key=?', (key,))
#         self._store.commit()
#
#     def __iter__(self):
#         for item in self._store.execute('SELECT key FROM shove'):
#             yield item
#
#     def __len__(self):
#         return self._store.execute('SELECT COUNT(*) FROM shove').fetchone()
#
#     def clear(self):
#         self._cursor.execute('DELETE FROM shove')
#         self._store.commit()