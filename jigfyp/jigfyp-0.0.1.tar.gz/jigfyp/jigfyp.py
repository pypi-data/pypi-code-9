import leveldb

class Jigfyp:
    def __init__(self, db, delimiter = b'!', highest_character = b'~'):
        '''
        Query your level database with tuples!

        :param leveldb.LevelDB db: The levelDB instance to query
        :param bytes delimiter: Character to delimit tuple elements in the keys
        :param bytes highest_character: Character for specifying the end of ranges
        '''
        self.db = db
        for name in ['delimiter', 'highest_character']:
            if not isinstance(locals()[name], bytes):
                raise TypeError('%s must be bytes.' % name)
            elif len(locals()[name]) != 1:
                raise ValueError('%s must have length 1.' % name)
            setattr(self, name, locals()[name])

    def put_one(db, key, value):
        '''
        Save a record to the level database.

        :type key: tuple of bytes
        :param key: The key
        :param bytes value: The value
        '''
        db.Put(_encode_key(self.delimiter, key), value)

    def put_many(db, pairs):
        '''
        Save a record to the level database.

        :type key: tuple of bytes
        :param key: The key
        :param bytes value: The value
        '''
        for key, value in pairs:
            batch.Put(_encode_key(self.delimiter, key), value)
        db.Write(batch)

    def get_one(db, key):
        '''
        Read one record from the level database.

        :type key: tuple of bytes
        :param key: The key
        :rtype: tuple containing two bytes elements
        :returns: The raw key and value corresponding to that key
        '''
        return db.Get(_encode_key(self.delimiter, key))

    def get_many(db, *key_prefix):
        '''
        Read several records from the level database. All records whose keys
        begin with the particular prefix are returned.

        :type key_prefix: tuple of bytes
        :param key_prefix: A left-aligned subset of the key values.
        :rtype: iterable of tuples, each containing two bytes elements
        :returns: Iterable of keys-value pairs
        '''
        keys = _encode_keys(self.delimiter, self.highest_character, key_prefix)
        for key, value in db.RangeIter(**keys):
            yield _decode_key(key), value

    def delete_one(db, key):
        '''
        Delete one record from the level database.

        :type key: tuple of bytes
        :param key: The key
        :rtype: None
        :returns: Nothing
        '''
        db.Delete(_encode_key(key))

    def delete_many(db, *key_prefix):
        '''
        Delete several records from the level database.

        :type key_prefix: tuple of bytes
        :param key_prefix: A left-aligned subset of the key values.
        :rtype: None
        :returns: Nothing
        '''
        keys = _encode_keys(self.delimiter, self.highest_character, key_prefix)
        for key, value in db.RangeIter(**keys):
            db.Delete(_encode_key(key))

def _encode_key(delimiter, key):
    return delimiter.join(key)

def _encode_keys(delimiter, highest_character, key):
    if len(key) > 0:
        key_from = _encode_key(delimiter, key)
        key_to = key_from + highest_character
    else:
        key_from = key_to = None

    return {
        'key_from': key_from,
        'key_to': key_to,
    }

def _decode_key(delimiter, x):
    return tuple(x.split(delimiter))
