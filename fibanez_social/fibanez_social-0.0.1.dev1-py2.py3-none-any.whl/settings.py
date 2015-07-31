"""Settings of Fibanez_social"""
from django.conf import settings

import os
gettext = lambda s: s
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'fibanez_social'
    ]

MIDDLEWARE_CLASSES = []

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite31'),
    }
}