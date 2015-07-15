import os.path
import re

from imhotep.tools import Tool

class JSCS(Tool):
    # Example: foo.js: line 5, col 3, Operator + should not stick ...etc
    response_format = re.compile(r'^(?P<filename>.*): ' \
        r'line (?P<line_number>\d+), col \d+, (?P<message>.*)$')
    file_extensions = ('.js',)

    def get_command(self, dirname, linter_configs=None):
        cmd = 'jscs -r inline'

        # If we have a config, use it. Otherwise, use airbnb style.
        config_path = os.path.join(dirname, '.jscsrc')
        if os.path.exists(config_path):
            cmd += ' -c %s' % config_path
        else:
            cmd += ' -p airbnb'
        return cmd
