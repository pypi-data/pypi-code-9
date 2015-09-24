import lnkr
from toml_config import TomlConfig
from export_section import ExportSection, new_export_section

class PackageConfig(TomlConfig):
    def __init__(self, path):
        self.attribs = {}
        self.export_sections = []
        self.wrapper_sections = []
        TomlConfig.__init__(self, path)

    def parse(self):
        lnkr.verbose('\nParse Package Config: %s' % lnkr.format_path(self.path))
        for key in self.values:
            value = self.values[key]
            if isinstance(value, dict):
                export_section = new_export_section(key, value)
                if export_section is not None:
                    self.export_sections.append(export_section)
            else:
                self.attribs[key] = value
        for key in self.attribs:
            lnkr.verbose('Parse Package Config Attrib: %s = %s' % (lnkr.format_path(key), lnkr.format_param(self.attribs[key])))
        for section in self.export_sections:
            lnkr.verbose('Parse Package Config Export Section: %s' % lnkr.format_param(section.__str__()))
        return len(self.export_sections) > 0

    def get_export_section(self, key):
        for section in self.export_sections:
            if section.key == key:
                return section
        return None
