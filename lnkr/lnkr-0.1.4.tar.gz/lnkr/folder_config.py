import os

import lnkr
import term

KEY_FROM = 'from'
KEY_TO = 'to'

class FolderConfig:
    def __init__(self, values):
        self.values = values
        self.valid = self.parse()

    def get_section_value(self, key, optional=False):
        return lnkr.get_section_value('FolderConfig', self.values, key, optional)

    def parse(self):
        self.from_value = self.get_section_value(KEY_FROM, True)
        self.to_value = self.get_section_value(KEY_TO, True)

        if self.from_value is None or self.to_value is None:
            term.error('Need to provide both "from" and "to": %s' % term.format_param(self.key))
            return False

        return True

    def get_from_path(self, root_path):
        return os.path.join(root_path, self.from_value)

    def get_to_path(self, root_path, attribs_holders):
        to_path = os.path.join(root_path, self.to_value)
        attribs = lnkr.get_attribs(attribs_holders)
        for key in attribs:
            old_to_path = to_path
            to_path = to_path.replace('${%s}' % key, attribs[key])
            term.verbose('\nUpdate Path: %s = %s\n\tFrom: %s\n\tTo: %s' % (term.format_param(key), term.format_param(attribs[key]), term.format_path(old_to_path), term.format_path(to_path)))
        return to_path
