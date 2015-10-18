import yaml


class ReadConfig:
    '''read config from .yaml config file
    '''
    def __init__(self, config_file_src, config=None):
        self.config_file = open(config_file_src, 'r')
        self._config = self._read_config()

    def __del__(self):
        if not self.config_file.closed:
            self.config_file.close()

    def _read_config(self):
        return yaml.load(self.config_file)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def get_config_keys(self):
        return list(self._config.keys())
