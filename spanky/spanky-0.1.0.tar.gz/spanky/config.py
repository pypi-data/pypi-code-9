"""
Create our config based on $base/etc/spanky

Generally, config files should be YAML or scripts.
"""
import os
import yaml


class BaseConfig(object):

    def __init__(self, path):
        self.path = path

    def __call__(self):
        """load our config"""
        raise NotImplemented


class YAMLConfig(BaseConfig):

    def __call__(self):
        return yaml.safe_load(open(self.path))


class ScriptConfig(BaseConfig):

    def __call__(self):
        return self

    def run(self):
        raise NotImplemented



class ConfigLoader(object):

    def __init__(self, path):
        self.path = path

    def config_type(self):
        if self.path.endswith('.yml') or self.path.endswith('.yaml'):
            return 'yaml'
        return 'script'

    @property
    def type(self):
        if not hasattr(self, '_type'):
            self._type = self.config_type()
        return self._type

    def __call__(self):

        if self.type == 'yaml':
            config = YAMLConfig(self.path)
        else:
            config = ScriptConfig(self.path)

        return config()


class Config(object):
    def __init__(self, base='/'):
        self.base = base

    def load(self, path):
        loader = ConfigLoader(os.path.join(self.base, path))
        return loader()
