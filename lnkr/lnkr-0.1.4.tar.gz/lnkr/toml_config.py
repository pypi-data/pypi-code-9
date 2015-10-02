import os

import pytoml

import lnkr
import term

class TomlConfig:
    def __init__(self, path):
        path = os.path.abspath(path)
        self.path = path
        self.root_path = os.path.dirname(path)
        self.values = None
        if not os.path.isfile(self.path):
            term.verbose('File Not Exist: %s' % term.format_path(self.path))
            self.valid = False
        else:
            self.valid = self.load() and self.parse()
            if not self.valid:
                term.error('Invalid Config [%s]: %s' % (self.__class__, term.format_path(self.path)))

    def load(self):
        try:
            self.values = pytoml.load(open(self.path, 'rb'))
        except Exception as e:
            term.error('Failed Loading Toml Config: %s' % term.format_path(self.path))
            return False
        return True

    def parse(self):
        return True
