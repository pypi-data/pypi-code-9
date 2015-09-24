import lnkr
from app_config import AppConfig

class WrapperConfig(AppConfig):
    def __init__(self, path):
        self.kind = 'Wrapper'
        AppConfig.__init__(self, path)

    def set_mode(self, mode):
        for section in self.import_sections:
            section.mode = mode

    def get_wrapper_section(self, key):
        return self.get_import_section(key)

