import logging
import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format': "[%(asctime)s] [%(log_color)s%(levelname)s%(reset)s] %(message)s",
            'log_colors': {
                'DEBUG': 'bold_black',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        }
    },
    'handlers': {
        # 'file': {
        #     'level': 'INFO',
        #     'class': 'logging.FileHandler',
        #     'filename': 'lisa_api.log',
        #     'formatter': 'color'
        # },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color'
        }
    },
    'loggers': {
        'lisa_api': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },

        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('lisa_api')
