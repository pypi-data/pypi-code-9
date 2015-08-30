from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from solo.models import SingletonModel
from django.db import models

def _get_content_type(cls):
    if cls._content_type is None:
        cls._content_type = ContentType.objects.get_for_model(cls)
    return cls._content_type

def _get_global_settings_models(cls):
    if cls._global_settings_models is None:
        cls._global_settings_models = [model for model in cls.__subclasses__()]
    return cls._global_settings_models

def _get_global_settings_content_types(cls):
    if cls._global_settings_content_types is None:
        cls._global_settings_content_types = [model.get_content_type() for model in cls.get_global_settings_models()]
    return cls._global_settings_content_types

class AbstractGlobalSettingsCollection(SingletonModel):
    _global_settings_models = None
    _global_settings_content_types = None
    _content_type = None
    
    get_content_type = classmethod(_get_content_type)
    get_global_settings_models = classmethod(_get_global_settings_models)
    get_global_settings_content_types = classmethod(_get_global_settings_content_types)
    
    class Meta:
        abstract = True

class AbstractSiteSettingsCollectionQuerySet(models.QuerySet):
    def for_site(self, site):
        obj, created = self.get_or_create(site=site)  # @UnusedVariable
        return obj

class AbstractSiteSettingsCollection(models.Model):
    site = models.OneToOneField('wagtailcore.Site',
            null=False,
            blank=False,
            unique=True,
            db_index=True,
            editable=False,
            on_delete=models.CASCADE,
            related_name='+',
            verbose_name=_('Site'))
    
    objects = AbstractSiteSettingsCollectionQuerySet.as_manager()
    
    _global_settings_models = None
    _global_settings_content_types = None
    _content_type = None
    
    get_content_type = classmethod(_get_content_type)
    get_global_settings_models = classmethod(_get_global_settings_models)
    get_global_settings_content_types = classmethod(_get_global_settings_content_types)
    
    class Meta:
        abstract = True
