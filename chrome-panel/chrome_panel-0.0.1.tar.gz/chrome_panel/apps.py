from django.apps import AppConfig

from chrome_panel import settings as cp_settings


class ChromePanelConfig(AppConfig):
    name = 'chrome_panel'
    verbose_name = "Chrome Debug Panel"

    def ready(self):
        cp_settings.patch_all()
