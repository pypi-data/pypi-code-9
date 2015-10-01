# -*- coding: utf-8 -*-

from kway import settings
from kway.models import KText

try: 
    
    from modeltranslation.translator import translator, TranslationOptions
    
    
    class KTextTranslationOptions(TranslationOptions):
        
        if settings.KWAY_USE_MODELTRANSLATION:
            fields = ('value', )
        else:
            fields = ()
            
    translator.register(KText, KTextTranslationOptions)
    
    
except ImportError:
    
    pass

    