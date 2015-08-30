from django import template
from wagtail_global_settings.models import AbstractSiteSettingsCollection
from wagtail.wagtailcore.models import Site

register = template.Library()

_site_settings_cache = None

def _get_components(app_label, model_name=None, field_name=None):
    if app_label is not None and model_name is None and field_name is None:
        components = unicode(app_label).split('.')
        if len(components) < 2:
            return u''
        app_label = components[0]
        model_name = components[1]
        field_name = components[2] if len(components) > 2 else None
    return app_label, model_name, field_name

def _get_site_settings_cache():
    global _site_settings_cache
    if _site_settings_cache is None:
        site_settings = {}
        for model in AbstractSiteSettingsCollection.get_global_settings_models():
            if model.get_content_type().app_label not in site_settings:
                site_settings[model.get_content_type().app_label] = {}
            site_settings[model.get_content_type().app_label][model.__name__] = model
        _site_settings_cache = site_settings
    return _site_settings_cache

def _get_site_setting(site, app_label, model_name, field_name=None):
    site_settings = _get_site_settings_cache()
    if app_label in site_settings and model_name in site_settings[app_label]:
        model = site_settings[app_label][model_name]
        if issubclass(model, AbstractSiteSettingsCollection):
            instance = model.objects.for_site(site)
            if field_name is None:
                return instance
            else:
                return getattr(instance, field_name, u'')
        else:
            return u''
    else:
        return u''

@register.simple_tag(name='site_settings', takes_context=True)
def _site_settings(context, app_label, model_name=None, field_name=None, site=None):
    if site is None or not isinstance(site, Site):
        site = context['request'].site
    return _get_site_setting(site, *_get_components(app_label, model_name, field_name))

@register.assignment_tag(name='get_site_settings', takes_context=True)
def _get_site_settings(context, app_label, model_name=None, field_name=None, site=None):
    if site is None or not isinstance(site, Site):
        site = context['request'].site
    return _get_site_setting(site, *_get_components(app_label, model_name, field_name))
