# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save

from kway import cache, settings, utils

try:
    from sorl.thumbnail import ImageField
    
except ImportError:    
    
    from django.db.models import ImageField
    

class KImage(models.Model):
    
    key = models.CharField(max_length = 100, unique = True, verbose_name = 'Key')
    value = ImageField(blank = True, default = '', upload_to = 'uploads/kway/images/', verbose_name = 'Value')
    
    class Meta:
        app_label = 'kway'
        ordering = ['key']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        
    def __unicode__(self):
        
        return unicode(u'[%s] - %s' % (self.key, self.value, ))


class KText(models.Model):
    
    key = models.CharField(max_length = 100, unique = True, verbose_name = 'Key')
    value = models.TextField(blank = True, default = '', verbose_name = 'Value')
    
    class Meta:
        app_label = 'kway'
        ordering = ['key']
        verbose_name = 'Text'
        verbose_name_plural = 'Texts'
        
    def __unicode__(self):
        
        return unicode(u'[%s] - %s' % (self.key, self.value, ))

        
if not settings.KWAY_USE_MODELTRANSLATION:
    
    #http://www.mixedcase.nl/articles/2009/11/26/how-dynamically-add-fields-django-model/
    for language in settings.KWAY_LANGUAGES:
        
        value_field_name = utils.get_localized_value_field_name(language[0])
        value_field_obj = models.TextField(blank = True, default = '', verbose_name = 'Value [%s]' % language[0])
        
        KText.add_to_class(value_field_name, value_field_obj)
    
    
post_save.connect(cache.update_values_post_save, sender = KText)

