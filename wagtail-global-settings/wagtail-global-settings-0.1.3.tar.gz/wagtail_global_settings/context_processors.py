from wagtail_global_settings.models import AbstractGlobalSettingsCollection,\
    AbstractSiteSettingsCollection

def global_settings(request):
    settings = {}
    for model in AbstractGlobalSettingsCollection.get_global_settings_models():
        if model.get_content_type().app_label not in settings:
            settings[model.get_content_type().app_label] = {}
        settings[model.get_content_type().app_label][model.__name__] = model.get_solo()
    return {
        'global_settings': settings
    }

def site_settings(request):
    if request is None or request.site is None:
        raise Exception, "Please add 'wagtail_global_settings.context_processors.site_settings' after 'django.template.context_processors.request'"
    settings = {}
    for model in AbstractSiteSettingsCollection.get_global_settings_models():
        if model.get_content_type().app_label not in settings:
            settings[model.get_content_type().app_label] = {}
        settings[model.get_content_type().app_label][model.__name__] = model.objects.for_site(request.site)
    return {
        'site_settings': settings
    }
