from django.apps import apps
from django.contrib import admin


def registerAdminSite(appName, excludeModels=[]):
    """Registers the models of the app with the given "appName" for the admin site"""
    for model in apps.get_app_config(appName).get_models():
        if model not in excludeModels:
            admin.site.register(model)
