import os

import lnkr
import term
from toml_config import TomlConfig
from import_section import ImportSection, new_import_section

class AppConfig(TomlConfig):
    def __init__(self, path):
        if not hasattr(self, 'kind'):
            self.kind = "App"
        self.attribs = {}
        self.import_sections = []
        self.linked_components = {}
        TomlConfig.__init__(self, path)

    def parse(self):
        term.verbose('\nParse %s Config: %s' % (self.kind, term.format_path(self.path)))
        for key in self.values:
            value = self.values[key]
            if isinstance(value, dict):
                import_section = new_import_section(self.root_path, key, value)
                if import_section is not None:
                    self.import_sections.append(import_section)
            else:
                self.attribs[key] = value
        for key in self.attribs:
            term.verbose('Parse %s Config Attrib: %s = %s' % (self.kind, term.format_path(key), term.format_param(self.attribs[key])))
        for section in self.import_sections:
            term.verbose('Parse %s Config Import Section: %s' % (self.kind, term.format_param(section.__str__())))
        return len(self.import_sections) > 0

    def get_import_section(self, key):
        for section in self.import_sections:
            if section.key == key:
                return section
        return None

    def mark_linked_component(self, key, section):
        self.linked_components[key] = section

    def is_component_linked(self, key):
        return self.linked_components.has_key(key)
