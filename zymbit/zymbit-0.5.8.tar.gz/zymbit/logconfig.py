import logging.config
import os
import sys

from zymbit.util import is_interactive

LOGLEVEL = os.environ.get('LOGLEVEL', 'info')
LOGFILE = os.environ.get('LOGFILE')


def config_logging(logfile=None, loglevel=None):
    logging.captureWarnings(True)

    logging.config.dictConfig(get_logging_config(logfile, loglevel))


def get_logging_config(logfile=None, loglevel=None):
    logfile = logfile or LOGFILE
    loglevel = (loglevel or LOGLEVEL).upper()

    syslog_device_path = '/dev/log'
    if sys.platform == 'darwin':
        syslog_device_path = '/var/run/syslog'

    logging_config = {
        'version': 1,
        'disable_existing_loggers': True,

        'formatters': {
            'default': {
                'format': '%(levelname)s %(asctime)s %(name)s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },

        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': loglevel,
                'stream': 'ext://sys.stdout',
                'formatter': 'default',
            },
            'syslog': {
                'class': 'logging.handlers.SysLogHandler',
                'level': loglevel,
                'address': syslog_device_path,
                'formatter': 'default',
            },
            'null': {
                'class': 'logging.NullHandler',
                'level': 'DEBUG',
            },
        },

        'loggers': {
            '': {
                'handlers': [],
                'propagate': True,
                'level': loglevel,
            },
            'filer': {
                'handlers': [],
                'propagate': False,
                'level': loglevel,
            },
            'requests': {
                'handlers': ['null'],
                'propagate': False,
                'level': 'ERROR',
            },
        },
    }

    if (is_interactive() and not logfile) or logfile == '-':  # log to the console when - is given as the logfile
        logging_config['loggers']['']['handlers'].append('console')
        logging_config['loggers']['filer']['handlers'].append('console')

        logging_config['handlers']['console'].update({
            'stream': 'ext://sys.stderr',
        })
    elif logfile:  # any other logfile setup a rotating file handler
        logging_config['handlers'].update({
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': logfile,
                'maxBytes': 1024 * 100,
                'backupCount': 2,
            },
        })

        logging_config['loggers']['']['handlers'].append('file')
        logging_config['loggers']['filer']['handlers'].append('file')
    else:  # log to syslog by default
        logging_config['loggers']['']['handlers'].append('syslog')
        logging_config['loggers']['filer']['handlers'].append('syslog')

    return logging_config
