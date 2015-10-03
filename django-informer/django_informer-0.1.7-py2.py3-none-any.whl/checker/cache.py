# coding: utf-8

"""django informer checker for Cache"""

from __future__ import absolute_import

from django.core.cache import cache

from informer.checker.base import BaseInformer, InformerException


class CacheInformer(BaseInformer):
    """
    Cache Informer.
    """

    def __str__(self):
        return u'Check if Cache is operational.'

    def check(self):
        """
        Perform check against default cache configuration
        """
        try:
            cache.set('foo', 'bar', 30)
            cache.get('foo')
        except Exception as error:
            raise InformerException(
                'An error occured when trying access cache: %s.' % error)
        else:
            return True, 'Your cache system is operational.'
