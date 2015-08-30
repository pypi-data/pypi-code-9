from django import template
from wagtail_global_settings.models import AbstractGlobalSettingsCollection

register = template.Library()

_global_settings_cache = None

def _get_components(app_label, model_name=None, field_name=None):
    if app_label is not None and model_name is None and field_name is None:
        components = unicode(app_label).split('.')
        if len(components) < 2:
            return u''
        app_label = components[0]
        model_name = components[1]
        field_name = components[2] if len(components) > 2 else None
    return app_label, model_name, field_name

def _get_global_settings_cache():
    global _global_settings_cache
    if _global_settings_cache is None:
        global_settings = {}
        for model in AbstractGlobalSettingsCollection.get_global_settings_models():
            if model.get_content_type().app_label not in global_settings:
                global_settings[model.get_content_type().app_label] = {}
            global_settings[model.get_content_type().app_label][model.__name__] = model
        _global_settings_cache = global_settings
    return _global_settings_cache

def _get_global_setting(app_label, model_name, field_name=None):
    _global_settings = _get_global_settings_cache()
    if app_label in _global_settings and model_name in _global_settings[app_label]:
        model = _global_settings[app_label][model_name]
        if issubclass(model, AbstractGlobalSettingsCollection):
            instance = model.get_solo()
            if field_name is None:
                return instance
            else:
                return getattr(instance, field_name, u'')
        else:
            return u''
    else:
        return u''

@register.simple_tag(name='global_settings')
def _global_settings(app_label, model_name=None, field_name=None):
    return _get_global_setting(*_get_components(app_label, model_name, field_name))

@register.assignment_tag(name='get_global_settings')
def _get_global_settings(app_label, model_name=None, field_name=None):
    return _get_global_setting(*_get_components(app_label, model_name, field_name))
