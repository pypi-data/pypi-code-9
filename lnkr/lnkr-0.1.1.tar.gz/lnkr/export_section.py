import os
import lnkr

from folder_config import FolderConfig
from file_config import FileConfig

KEY_FOLDERS = 'folders'
KEY_FILES = 'files'
KEY_REQUIRES = 'requires'

class ExportSection:
    def __init__(self, key, values):
        self.key = key
        self.values = values
        self.folders = []
        self.files = []
        self.requires = []
        self.valid = self.parse()

    def __str__(self):
        if self.valid:
            return '[%s] -> {len(folders) = %s, len(files) = %s, len(requires) = %s}' % (self.key, len(self.folders), len(self.files), len(self.requires))
        else:
            return 'Invalid: [%s] -> %s' % (self.key, self.values)

    def get_section_value(self, key, optional=False):
        return lnkr.get_section_value('ExportSection', self.values, key, optional)

    def parse(self):
        self.folders = []
        folders_values_list = self.get_section_value(KEY_FOLDERS, True)
        if folders_values_list is not None:
            for values in folders_values_list:
                folder = FolderConfig(values)
                if folder.valid:
                    self.folders.append(folder)

        self.files = []
        files_values_list = self.get_section_value(KEY_FILES, True)
        if files_values_list is not None:
            for values in files_values_list:
                fc = FileConfig(values)
                if fc.valid:
                    self.files.append(fc)

        #TODO: validate requires
        self.requires = self.get_section_value(KEY_REQUIRES, True) or []

        if len(self.folders) == 0 and len(self.files):
            lnkr.error('Need to provide either "folders" or "files": %s' % lnkr.format_param(self.key))
            return False

        return True


def new_export_section(key, values):
    section = ExportSection(key, values)
    if section.valid:
        return section
    else:
        lnkr.error('Invalid Export Section: %s -> %s' % (key, values))
