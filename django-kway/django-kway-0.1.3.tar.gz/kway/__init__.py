# -*- coding: utf-8 -*-

from django.utils import translation

from kway import cache
from kway.models import KImage, KText
from kway import localization
from kway import settings
from kway.version import __version__


def kgetimage( key, *args, **kwargs ):

    obj, obj_created = KImage.objects.get_or_create(key = key)

    return obj.value.url if obj.value else ''


def kgettext( key, key_plural = None, count = None, *args, **kwargs ):
    
    value_args = kwargs.copy()
    
    if 'default' in value_args:
        del(value_args['default'])
        
    if count != None:
        
        count = int(count)
        
        if not 'count' in value_args:
            value_args['count'] = count
        
        if not 'n' in value_args:
            value_args['n'] = count
            
        abs_count = (count if count >= 0 else -count)
        
        plural_form = localization.get_plural_form(translation.get_language(), abs_count)
        
        key = key_plural if key_plural and plural_form > 0 else key
        
        try:
            key = key % str(plural_form)
        
        except KeyError:
            pass
            
        except ValueError:
            pass
        
    value = cache.get_value_for_key(key)

    key_value = (key if settings.KWAY_USE_KEY_AS_VALUE else '')
    
    default_value = kwargs.get('default', (key if settings.KWAY_USE_KEY_AS_DEFAULT_VALUE else ''))
    
    debug_value = ('[[ ' + key + ' ]]' if settings.KWAY_USE_KEY_AS_DEBUG_VALUE else '')
    
    if not value:
        
        obj, obj_created = KText.objects.get_or_create(key = key, defaults = { 'value':default_value })
        
        value = obj.value
        
        cache.set_value_for_key(key, value)
        
    value = (value or key_value or debug_value)
    
    if len(value_args.keys()):
        
        try:
            value = value % value_args
        
        except KeyError:
            pass
            
        except ValueError:
            pass
            
    return value
    
    