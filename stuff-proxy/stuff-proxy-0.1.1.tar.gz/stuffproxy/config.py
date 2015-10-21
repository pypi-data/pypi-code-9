import os

from yamlsettings import YamlSettings


class Settings(object):
    def __init__(self):
        self.settings = None

    def configure(self, filename):
        self.settings = YamlSettings(os.path.join(os.path.dirname(__file__), 'defaults.yml'), filename).get_settings()

    def __getattr__(self, item):
        return getattr(self.settings, item)


settings = Settings()