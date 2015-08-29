from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType
from solo.models import SingletonModel

class AbstractGlobalSettingsCollection(SingletonModel):
    _global_settings_models = None
    _global_settings_content_types = None
    _content_type = None
    
    @classmethod
    def get_content_type(cls):
        if cls._content_type is None:
            cls._content_type = ContentType.objects.get_for_model(cls)
        return cls._content_type
    
    @classmethod
    def get_global_settings_models(cls):
        if cls._global_settings_models is None:
            cls._global_settings_models = [model for model in cls.__subclasses__()]
        return cls._global_settings_models
    
    @classmethod
    def get_global_settings_content_types(cls):
        if cls._global_settings_content_types is None:
            cls._global_settings_content_types = [model.get_content_type() for model in cls.get_global_settings_models()]
        return cls._global_settings_content_types
    
    class Meta:
        abstract = True