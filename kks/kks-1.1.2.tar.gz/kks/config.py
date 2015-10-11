# coding=utf8

"""
    kks.config
    ~~~~~~~~~~

    Configuration manager, kks's configuration is in toml.
"""

from os.path import exists

from . import charset
from .exceptions import ConfigSyntaxError
from .utils import join

import toml


class Config(object):

    filename = 'config.toml'
    filepath = join('.', filename)

    # default configuration
    default = {
        'root': '',
        'blog': {
            'short_name': '',
            'long_name': '',
            'theme': 'theme',
        },
        'author': {
            'name': '康凯森',
        },
    }

    def parse(self):
        """parse config, return a dict"""

        if exists(self.filepath):
            content = open(self.filepath).read().decode(charset)
        else:
            content = ""

        try:
            config = toml.loads(content)
        except toml.TomlSyntaxError:
            raise ConfigSyntaxError

        return config


config = Config()
