from . import info
import xdg.BaseDirectory
import os
import sys
import json


class Configuration:
    """
    A configuration class that stores options as properties.

    Attempts to load (module location)/default_config.json, then overrides
    those with those in the path argument

    Keyword arguments:
    TODO: should maybe be in __init__'s docstring
    path -- path to load the config override from

    Examples:
    (after creating $XDG_CONFIG_HOME/photonemitter/config.json)
    >>> cfg = Configuration()
    >>> cfg.foo
    'bar'
    """

    def __init__(self, path=os.path.join(
                 xdg.BaseDirectory.save_config_path(info.app_name),
                 'config.json'
                 )):
        self.path = path
        self._config = {}
        self._load(os.path.join(os.path.dirname(__file__),
                                'default_config.json'))
        self._load(self.path)

    def _load(self, path):
        try:
            with open(path) as h:
                self._config.update(json.load(h))
        except:
            print('CRITICAL: error while loading config file {}'.format(path),
                  file=sys.stderr)
            raise
        for var, val in self._config.items():
            setattr(self, var, val)
