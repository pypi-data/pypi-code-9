import sys

import six

from .utils import import_object

def register_default(key, val=None):
    KVStore.register(key, val)

class KVStore(object):

    alias = {
        'redis': 'waterboy.backends.RedisBackend',
        'mongo': 'waterboy.backends.MongoBackend',
        'dict': 'waterboy.backends.DictBackend',
    }
    _defaults = {}


    @classmethod
    def register(cls, key, default):
        """Register individual defaults by calling this method"""
        cls._defaults[cls.prefixed(key)] = default

    @classmethod
    def backend_instance(cls, constructor, params=None):
        if isinstance(constructor, six.string_types):
            try:
                # may be an alias
                constructor = cls.alias[constructor]
            except KeyError:
                pass
            if isinstance(constructor, six.string_types):
                constructor = import_object(constructor)
        if not params:
            instance = constructor()
        elif isinstance(params, list):
            instance = constructor(*params)
        elif isinstance(params, dict):
            instance = constructor(**params)
        else:
            instance = constructor(params)
        return instance

    def __init__(self, backend_class, backend_params=None, initial=None, prefix='', strict=True):
        """Initialise new config object.

        initial can be a module, class, dictionary (or anything with a
        '__dict__'), and may optionally be given as a "dotted string".

        """
        if isinstance(initial, six.string_types):
            try:
                __import__(initial)
            except ImportError:
                initial = import_object(initial)
            else:
                initial = sys.modules[initial]

        if hasattr(initial, '__dict__'):
            # class or module
            initial = initial.__dict__

        config = self._defaults.copy()
        for k, v in initial.items():
            if k and k.startswith(prefix):
                config[k] = v

        backend = self.backend_instance(backend_class, backend_params)

        # use self.__dict__ here so as not to invoke a recursive '__getattr__'
        self.__dict__['_config'] = config
        self.__dict__['_backend'] = backend
        self.__dict__['_prefix'] = prefix
        self.__dict__['_strict'] = strict

    def __getattr__(self, key):
        """Get a registered value from the associated backend."""
        prefixed_key = self.prefixed(key)
        try:
            default = self._config[prefixed_key]
        except KeyError:
            if self._strict:
                raise AttributeError(key)
            default = None
        val = self._backend.get(prefixed_key)
        if val is None:
            val = default
        return val

    def __setattr__(self, key, value):
        """Save a registered value to the associated backend."""
        prefixed_key = self.prefixed(key)
        if self._strict and prefixed_key not in self._config:
            raise AttributeError(key)
        return self._backend.set(key, value)

    def __dir__(self):
        return self._config.keys()

    def prefixed(self, key):
        """Prefixes keys if they are not already prefixed, so you have the
        option of getting or setting with or without a prefix.
        """
        if not key.startswith(self._prefix):
            key = self._prefix + key
        return key

    @property
    def backend(self):
        return self._backend

    def clear(self):
        self._backend.delete(*self._config.keys())

class DictConfig(KVStore):
    '''Dummy key/value store where the "backend" is just a python dictionary.'''

    def __init__(self, *args, **kwargs):
        super(DictConfig, self).__init__('dict', *args, **kwargs)

class RedisConfig(KVStore):
    """Redis-backed key/value store."""

    def __init__(self, *args, **kwargs):
        if args:
            connection = args[0]
            args = args[1:]
        else:
            connection = None
        super(RedisConfig, self).__init__('redis', connection, *args, **kwargs)

class MongoConfig(KVStore):
    """MongoDB-backed key/value store.

    The first argument to the constructor must be the name of a mongodb database.
    """

    def __init__(self, db, *args, **kwargs):
        if args:
            connection = args[0]
            args = args[1:]
        else:
            connection = None
        super(MongoConfig, self).__init__('mongo', [db, connection], *args, **kwargs)

