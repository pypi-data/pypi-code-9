import os
import inspect
import ConfigParser
import appdirs

from exceptions import ConfigError


class Config():
    def __init__(self, filename='config'):
        self._items = {}
        self._last_accessed = None
        self._filename = filename

        self.reload()

    def __getitem__(self, item):
        if not item in self._items:
            raise Exception('You are missing the \'%s\' block in your `config` file.' % item)
        return self._items[item]

    def reload(self):
        system_path = os.path.join(appdirs.site_config_dir('findex'), self._filename)
        user_path = os.path.join(appdirs.user_config_dir('findex'), self._filename)

        if not os.path.isfile(system_path) and not os.path.isfile(user_path):
            raise ConfigError('Could not load config file \'%s\' or \'%s\'.' % (system_path, user_path))

        cfg = ConfigParser.ConfigParser()
        cfg.read([system_path, user_path])

        data = {}
        for section in cfg.sections():
            data[section] = {}

            for k, v in cfg.items(section):
                if k.startswith('#') or v.startswith('#'):
                    continue

                if v:
                    try:
                        data[section][k] = int(v) if not '.' in v else float(v)
                        continue
                    except:
                        pass

                    if v.lower() == 'false':
                        data[section][k] = False
                        continue
                    elif v.lower() == 'true':
                        data[section][k] = True
                        continue

                data[section][k] = v

        self._items = data

    def get(self, section, item):
        try:
            return self._items[section][item]
        except:
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            raise Exception('Could not access config variable \'%s\' from section \'%s\' - Might want to check it out - Caller: %s' % (item, section, mod.__name__))
