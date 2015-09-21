# -*- coding: utf-8 -*-
import os
import re


FILE_PATH = '/etc/profile.d/env.sh'

if os.path.exists(FILE_PATH):
    try:
        f = open(FILE_PATH)
        for line in f:
            line = line.replace('\n','').replace('export ','')
            line = re.sub(r'^([A-Z\_]+)',r"os.environ['\1']",line)
            try:
                exec(line)
            except Exception, e:
                print line + " - ERRO: " + str(e)
    except Exception, e:
        print str(e)
        pass

os.environ['DJANGO_SETTINGS_MODULE'] = 'api_flask.settings'

SECRET_KEY = os.environ.get('SECRET_KEY')

ENVIRONMENT = os.environ.get('ENVIRONMENT')

if os.environ.get('DEBUG') == 'False':
    DEBUG = False
else:
    DEBUG = True

CHAVE_API = os.environ.get('CHAVE_API')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.environ.get('DATABASE_HOST'),
        "NAME": os.environ.get('DATABASE_NAME'),
        "PASSWORD": os.environ.get('DATABASE_PASSWORD'),
        "PORT": os.environ.get('DATABASE_PORT'),
        "USER": os.environ.get('DATABASE_USER'),
        "CONN_MAX_AGE": 60,
        "TIME_ZONE": 'America/Sao_Paulo'
    }
}

REDIS = {
    'HOST': os.environ.get('REDIS_HOST'),
    'PORT': os.environ.get('REDIS_PORT'),
    'DB': os.environ.get('REDIS_DB')
}

SENTRY_DSN_API = os.environ.get('SENTRY_DSN_API')

ELASTICSEARCH_ASSISTANCE_URL = os.environ.get('ELASTICSEARCH_ASSISTANCE_URL')
ELASTICSEARCH_EVIDENCE_URL = os.environ.get('ELASTICSEARCH_EVIDENCE_URL')

TIME_ZONE = 'America/Sao_Paulo'

LANGUAGE_CODE = 'pt-br'

MEDIA_URL = os.environ.get('MEDIA_URL')

TEMPLATE_DIRS = ('/opt/bucket.email.templates',)

LOG_LEVEL = 'DEBUG' if DEBUG else 'ERROR'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'django.request': {
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'django.db.backends': {
            'level': LOG_LEVEL,
            'handers': ['default'],
        }
    }
}
