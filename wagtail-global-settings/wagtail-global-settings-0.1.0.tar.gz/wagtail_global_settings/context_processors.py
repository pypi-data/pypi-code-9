from wagtail_global_settings.models import AbstractGlobalSettingsCollection

def global_settings(request):
    settings = {}
    for model in AbstractGlobalSettingsCollection.get_global_settings_models():
        if model.get_content_type().app_label not in settings:
            settings[model.get_content_type().app_label] = {}
        settings[model.get_content_type().app_label][model.__name__] = model.get_solo()
    return {
        'global_settings': settings
    }