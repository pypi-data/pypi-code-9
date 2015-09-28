import os
import lnkr

KEY_LOCAL = 'local'
KEY_REMOTE = 'remote'
KEY_MODE = 'mode'

MODE_COPY = 'copy'
MODE_LINK = 'link'
MODE_SYMLINK = 'symlink'

class ImportSection:
    def __init__(self, path, key, values):
        self.path = path
        self.key = key
        self.values = values
        self.valid = self.parse()
        self.loaded = False
        self.package_config = None
        self.wrapper_config = None

    def __str__(self):
        if self.valid:
            return '[%s] -> {local = "%s", remote = "%s", mode = "%s"}' % (self.key, self.local, self.remote, self.mode)
        else:
            return 'Invalid: [%s] -> %s' % (self.key, self.values)

    def get_section_value(self, key, optional=False):
        return lnkr.get_section_value('ImportSection', self.values, key, optional)

    def parse(self):
        self.local = self.get_section_value(KEY_LOCAL, True)
        self.remote = self.get_section_value(KEY_REMOTE, True)
        self.mode = self.get_section_value(KEY_MODE, True)

        if self.local is None and self.remote is None:
            lnkr.error('Need to provide either "local" or "remote": %s' % lnkr.format_param(self.key))
            return False

        return True

    def do_load(self, package_path):
        self.package_config = lnkr.load_package_config(package_path)

        self.wrapper_config = lnkr.load_wrapper_config(package_path)
        if self.wrapper_config is not None:
            self.wrapper_config.set_mode(self.mode)

        return self.package_config is not None

    def load_local(self):
        return self.do_load(os.path.join(self.path, self.local))

    def load_remote(self):
        lnkr.info('Not Implemented: Import Remote Package')
        return False

    def check_mode(self):
        if self.mode == MODE_COPY:
            return True
        elif self.mode == MODE_LINK:
            return True
        elif self.mode == MODE_SYMLINK:
            return True

        return False

    def load(self):
        if not self.check_mode():
            return False

        if self.local is not None:
            self.loaded = self.load_local()
        elif self.remote is not None:
            self.loaded = self.load_remote()
        if not self.loaded:
            lnkr.error('Load Import Section Failed: %s' % lnkr.format_param(self.key))

    def get_component(self, key):
        export_section = self.package_config.get_export_section(key)
        if export_section is not None:
            return export_section
        elif self.wrapper_config is not None:
            wrapper_section = self.wrapper_config.get_wrapper_section(key)
            if wrapper_section is not None:
                return wrapper_section
        return None

def new_import_section(path, key, values):
    section = ImportSection(path, key, values)
    if section.valid:
        return section
    else:
        lnkr.error('Invalid Import Section: %s -> %s' % (key, values))
