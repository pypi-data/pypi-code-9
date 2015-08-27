# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS.
# This code is distributed under the two-clause BSD License.
from __future__ import absolute_import, unicode_literals
import base64
import logging

from getconf import ConfigGetter
from sentry.conf.server import *

from autoguard.config_helpers import (
    database_from_url, get_hostname, mail_from_url, sentry_caches_from_url,
    ldapized_middleware_classes, ldapized_authentication_backends
)


PROJECT_NAME = 'autoguard'
CONFIG = ConfigGetter(
    PROJECT_NAME,
    ['/etc/%s/' % PROJECT_NAME, 'local_settings.ini'],
    {
        'DEFAULT': {
            'host': '127.0.0.1',
            'port': 9000,
        },
        'dev': {
            'debug': False,
            'template_debug': False,
            'maintenance': False,
        },
        'django': {
            'broker_url': None,
            'db_uri': 'sqlite:///autoguard.sqlite',
            'mail_uri': 'console://?sender=no-reply@localhost',
            'site_url': 'http://localhost:9000',
            'secret_key':  base64.b64encode(os.urandom(40)),
            'time_zone': 'UTC',
            'language_code': 'fr-FR',
        },
        'ldap': {
            'uri': None,
            'user_tpl': 'uid={username}',
            'user_key': 'uniqueMember',
            'groups': '',
        },
        'sentry': {
            'cache_url': 'redis://127.0.0.1:6379/',
            'web_workers': 5,
        }
    }
)

# Locale Setup
# ############

TIME_ZONE = CONFIG.get('django.time_zone')
LANGUAGE_CODE = CONFIG.get('django.language_code')

# Database and Caches Setup
# #########################

DATABASES = {
    'default': database_from_url(CONFIG.get('django.db_uri'))
}

_parsed_sentry_caches = sentry_caches_from_url(CONFIG.get('sentry.cache_url'))
CACHES = _parsed_sentry_caches['django_caches']
SENTRY_REDIS_OPTIONS = _parsed_sentry_caches['redis_options']
SENTRY_CACHE = _parsed_sentry_caches['sentry']
SENTRY_BUFFER = _parsed_sentry_caches['buffer']
SENTRY_TSDB = _parsed_sentry_caches['tsdb']
SENTRY_RATELIMITER = _parsed_sentry_caches['rate_limits']


# Email setup
# ###########

_parsed_email_url = mail_from_url(CONFIG.get('django.mail_uri'))
EMAIL_SUBJECT_PREFIX = _parsed_email_url['prefix']
EMAIL_BACKEND = _parsed_email_url['backend']
EMAIL_HOST = _parsed_email_url['host']
EMAIL_PORT = _parsed_email_url['port']
EMAIL_HOST_USER = _parsed_email_url['user']
EMAIL_HOST_PASSWORD = _parsed_email_url['password']
EMAIL_USE_TLS = _parsed_email_url['use_tls']
SERVER_EMAIL = _parsed_email_url['sender']


# Async Setup
# ###########

BROKER_URL = CONFIG.get('django.broker_url')
CELERY_ALWAYS_EAGER = BROKER_URL is not None


# Web Server Setup
# ################

STATIC_URL = '/static/'
SENTRY_URL_PREFIX = CONFIG.get('django.site_url')

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", get_hostname(SENTRY_URL_PREFIX)]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

SENTRY_WEB_HOST = CONFIG.get('host')
SENTRY_WEB_PORT = CONFIG.getint('port')
SENTRY_WEB_OPTIONS = {
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
    'workers': CONFIG.getint('sentry.web_workers'),
}

SECRET_KEY = CONFIG.get('django.secret_key')


# Sentry Setup
# ############

SENTRY_USE_BIG_INTS = True
SENTRY_BEACON = False

SENTRY_ALLOW_REGISTRATION = False  # no auto-registration
SOCIAL_AUTH_CREATE_USERS = False  # no auto-registration

# LDAP Setup
# ##########

LDAP = {
    'uri': CONFIG.get('ldap.uri'),
    'user_tpl': CONFIG.get('ldap.user_tpl'),
    'member_key': CONFIG.get('ldap.member_key'),
    'groups': [x.strip() for x in CONFIG.get('ldap.groups').split(';')],
}

if LDAP['uri']:
    MIDDLEWARE_CLASSES = ldapized_middleware_classes(MIDDLEWARE_CLASSES)
    AUTHENTICATION_BACKENDS = ldapized_authentication_backends(AUTHENTICATION_BACKENDS)

# Dev Setup
# #########

DEBUG = CONFIG.getbool('dev.debug')
TEMPLATE_DEBUG = CONFIG.getbool('dev.template_debug')
MAINTENANCE = CONFIG.getbool('dev.maintenance')

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
