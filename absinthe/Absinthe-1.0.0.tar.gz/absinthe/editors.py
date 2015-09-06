import subprocess
from abc import abstractmethod

from window_manager import WindowManager

class EditorBase(object):
    def __init__(self, name, bin_path, logger):
        self.name = name
        self.bin_path = bin_path
        self.logger = logger

    @abstractmethod
    def open_content(self, content):
        pass

    @abstractmethod
    def set_focus(self):
        pass

    @abstractmethod
    def get_command_pattern(self):
        return []

    def open_file(self, filename, line):
        command = []
        data = dict(filename = filename, line = line)
        for pattern in self.get_command_pattern():
            command.append(pattern % data)

        self.logger.debug('Call command to open file: %s' % command)

        try:
            subprocess.call(command)
        except Exception as e:
            self.logger.error('Editor command failed: %s' % e)


class Notepadpp(EditorBase):
    def __init__(self, *args):
        super(Notepadpp, self).__init__(*args)
        self.winmgr = WindowManager()

    def get_command_pattern(self):
        return [self.bin_path, "%(filename)s", "-n%(line)d"]

    def open_content(self, content):
        pass

    def set_focus(self):
        self.winmgr.find_window_regex(".*Notepad\+\+")
        self.winmgr.set_foreground()