import sys
import yaml
import logging
import logging.config
import pkg_resources

class MultiLineFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        # hack: http://stackoverflow.com/a/5879524/533618
        backup_exc_text = record.exc_text
        record.exc_text = None
        formatted = logging.Formatter.format(self, record)
        message = record.getMessage()
        if message == '':
            header = formatted
        else:
            header = formatted.split(record.message)[0]
        record.exc_test = backup_exc_text
        return header + ('\n' + header).join(it for it in record.getMessage().split('\n') if it)

class LevelFilter(logging.Filter):
    def __init__(self, levels):
        self.levels = [logging._levelNames[it] for it in levels]

    def filter(self, record):
        return record.levelno in self.levels

class NotLevelFilter(logging.Filter):
    def __init__(self, levels):
        self.levels = [logging._levelNames[it] for it in levels]

    def filter(self, record):
        return record.levelno not in self.levels

def read_yaml_config(f):

    if isinstance(f, basestring):
        f = open(f, 'r')

    D = yaml.load(f)
    D.setdefault('version', 1)
    D.setdefault('disable_existing_loggers', True)
    logging.config.dictConfig(D)

    f.close()

def get_logger(profile='default', config_filename=None):

    try:
        if config_filename is not None:
            read_yaml_config(config_filename)
        else:
            filestream = pkg_resources.resource_stream(__name__, 'cfg/logging.yml')
            read_yaml_config(filestream)

        my_logger = logging.getLogger(profile)
        assert isinstance(my_logger, object)
        return my_logger
    except Exception as e:
        sys.stderr.write("ERROR: cannot configure logger with '{}': {}\n".format(config_filename, e))
        raise