import configparser


class ConfigParser(configparser.ConfigParser):
    def getboolean(self, *args, **kwargs):
        try:
            return super(ConfigParser, self).getboolean(*args, **kwargs)
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    def getstring(self, *args, **kwargs):
        try:
            return super(ConfigParser, self).get(*args, **kwargs)
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    def getint(self, *args, **kwargs):
        try:
            return super(ConfigParser, self).getint(*args, **kwargs)
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass

    def getfloat(self, *args, **kwargs):
        try:
            return super(ConfigParser, self).getfloat(*args, **kwargs)
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass
