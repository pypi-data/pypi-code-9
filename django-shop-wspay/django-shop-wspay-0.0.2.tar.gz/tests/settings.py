# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def ABS_PATH(*args):
    return os.path.join(ROOT_DIR, *args)


LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
]

DEBUG = True
TEMPLATE_DEBUG = True

FIXTURE_DIRS = (
    ABS_PATH('tests', 'fixtures'),
)

USE_TZ = True

ROOT_URLCONF = 'tests.urls'

SECRET_KEY = 'secretkey'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.admin',
    'shop',
    'shop_wspay',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
