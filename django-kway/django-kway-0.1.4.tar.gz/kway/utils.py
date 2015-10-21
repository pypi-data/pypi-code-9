# -*- coding: utf-8 -*-

from django.utils import translation

from kway import settings


def get_localized_key(key, language_code = None):
    
    language_code = (language_code or translation.get_language())
    language_key = language_code.replace('-', '_')
    
    localized_key = key + '_' + language_key
    
    return localized_key
    
    
__get_localized_value_field_name_proxy = get_localized_key

if settings.KWAY_USE_MODELTRANSLATION:
    
    try:
        from modeltranslation.utils import build_localized_fieldname as __get_localized_value_field_name_proxy
        
    except ImportError:
        pass
        
        
def get_localized_value_field_name(language_code = None):
    
    language_code = (language_code or translation.get_language())
    
    return __get_localized_value_field_name_proxy('value', language_code)
    
    