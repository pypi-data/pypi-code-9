import os
import formic

import lnkr
import term
from folder_config import FolderConfig

KEY_INCLUDE = 'include'
KEY_EXCLUDE = 'exclude'

class FileConfig(FolderConfig):
    def get_section_value(self, key, optional=False):
        return lnkr.get_section_value('FileConfig', self.values, key, optional)

    def parse(self):
        ok = FolderConfig.parse(self)
        if ok:
            self.include = self.get_section_value(KEY_INCLUDE, False)
            self.exclude = self.get_section_value(KEY_EXCLUDE, True)
        return ok

    def get_file_list(self, from_path):
        file_set = formic.FileSet(directory=from_path, include=self.include, exclude=self.exclude)
        return [os.path.relpath(file_name, from_path) for file_name in file_set]
