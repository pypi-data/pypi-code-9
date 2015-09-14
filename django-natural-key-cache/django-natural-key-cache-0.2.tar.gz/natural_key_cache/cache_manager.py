# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
natural_key_cache.cache_manager
===============================
'''
import hashlib
import django

if django.VERSION[:2] >= (1, 7):
    from django.core.cache import caches
else:
    from django.core.cache import get_cache as caches

from django.db import models
from django.db.models.manager import ManagerDescriptor

import logging
logger = logging.getLogger(__name__)


class NaturalKeyCacheManager(object):
    '''
    Custom model manager that allows for lookups via natural keys.
    '''
    DNE = 'DOES_NOT_EXIST'

    def __init__(self,
                 natural_keys=None,
                 backend='default',
                 timeout=None):
        if not natural_keys:
            natural_keys = [
                'pk',
            ]
        self.natural_keys = natural_keys
        if django.VERSION[:2] >= (1, 7):
            self.cache_backend = caches[backend]
        else:
            self.cache_backend = caches(backend)
        self.timeout = timeout

    def generate_key(self, **search_params):
        '''
        Build the cache key
        '''
        key_parts = ''.join(
            [u'{0}{1}'.format(k, v) for k, v in search_params.items()]
        )
        full_key = u'{model}{parts}'.format(
            model=self.model._meta.db_table,
            parts=key_parts,
        )
        return hashlib.md5(full_key.encode('utf-8')).hexdigest()

    def get(self, **kwargs):
        '''
        Get the object.

        Attempt to get the object from cache based on the natural keys.
        if not in cache, retrieve from database and cache the result.
        '''
        search_params = {}
        for key in self.natural_keys:
            search_params[key] = kwargs[key]
        cache_key = self.generate_key(**search_params)
        obj = self.cache_backend.get(cache_key)
        if obj is None:
            logger.debug('cache miss %s: %s',
                         self.model._meta.db_table,
                         cache_key)
            try:
                obj = self.model._default_manager.get(**search_params)
                self.cache_backend.set(cache_key, obj)
            except self.model.DoesNotExist:
                self.cache_backend.set(cache_key, self.DNE)
                raise
        elif obj == self.DNE:
            raise self.model.DoesNotExist()
        return obj

    def contribute_to_class(self, model, name):
        '''
        Settings applied to the model when using this manager
        '''
        self.model = model  # pylint: disable=attribute-defined-outside-init
        setattr(model, name, ManagerDescriptor(self))
        models.signals.post_save.connect(self.post_save, sender=model)
        models.signals.post_delete.connect(self.post_delete, sender=model)

    def post_save(self,
                  instance,
                  **kwargs):  # pylint: disable=unused-argument
        '''
        Update cache on post save
        '''
        search_params = {}
        for key in self.natural_keys:
            search_params[key] = getattr(instance, key)
        key = self.generate_key(**search_params)
        logger.debug('model %s saved: updating cache: %s',
                     instance._meta.db_table,
                     key)
        self.cache_backend.set(key, instance, self.timeout)

    def post_delete(self,
                    instance,
                    **kwargs):  # pylint: disable=unused-argument
        '''
        Update cache on post delete
        '''
        search_params = {}
        for key in self.natural_keys:
            search_params[key] = getattr(instance, key)
        key = self.generate_key(**search_params)
        logger.debug('model %s deleted: updating cache: %s',
                     instance._meta.db_table,
                     key)
        self.cache_backend.set(key, self.DNE, self.timeout)
