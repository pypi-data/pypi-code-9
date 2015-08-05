from logging import config


config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(levelname)s] %(name)s: %(message)s'
            },
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': "\t%(log_color)s%(message)s %(reset)s"
            }
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'colored',
            },
        },
        'loggers': {
            'okapi': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    }
)
