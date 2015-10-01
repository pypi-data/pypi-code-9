# -*- coding: utf-8 -*-

from django.conf import settings


KWAY_ADMIN_LIST_EDITABLE = getattr(settings, 'KWAY_ADMIN_LIST_EDITABLE', True)
KWAY_ADMIN_LIST_PER_PAGE = getattr(settings, 'KWAY_ADMIN_LIST_PER_PAGE', 100)

KWAY_CACHE_NAME = getattr(settings, 'KWAY_CACHE_NAME', 'kway')
KWAY_CACHE_KEY_PREFIX = getattr(settings, 'KWAY_CACHE_KEY_PREFIX', 'kway')
KWAY_CACHE_TIMEOUT =  getattr(settings, 'KWAY_CACHE_TIMEOUT', (60 * 60 * 24)) #1 day

__cache_backend = settings.CACHES.get(KWAY_CACHE_NAME, None)

if not __cache_backend:
    
    __cache_backend = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 
        'KEY_PREFIX': KWAY_CACHE_KEY_PREFIX, 
        'TIMEOUT': KWAY_CACHE_TIMEOUT
    }
    
    settings.CACHES[KWAY_CACHE_NAME] = __cache_backend
    
KWAY_LANGUAGES = getattr(settings, 'KWAY_LANGUAGES', settings.LANGUAGES)

if len(KWAY_LANGUAGES) > 0:
    for language in KWAY_LANGUAGES:
        if not language in settings.LANGUAGES:
            raise ValueError('KWAY_LANGUAGES cannot contain invalid languages: %s' % str(language))
else:
    raise ValueError('KWAY_LANGUAGES must contain at least 1 language')
    
KWAY_USE_KEY_AS_DEBUG_VALUE = getattr(settings, 'KWAY_USE_KEY_AS_DEBUG_VALUE', True) and settings.DEBUG
KWAY_USE_KEY_AS_DEFAULT_VALUE = getattr(settings, 'KWAY_USE_KEY_AS_DEFAULT_VALUE', False)
KWAY_USE_KEY_AS_VALUE = getattr(settings, 'KWAY_USE_KEY_AS_VALUE', False)

KWAY_USE_MODELTRANSLATION = ('modeltranslation' in settings.INSTALLED_APPS)

