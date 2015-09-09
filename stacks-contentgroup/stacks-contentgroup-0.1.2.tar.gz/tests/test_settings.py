from __future__ import unicode_literals

import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "rest_framework",
    "versatileimagefield",
    "textplusstuff",
    "stacks_contentgroup",
    "tests",
]


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

ROOT_URLCONF = 'tests.urls'
DEBUG = True
USE_TZ = True

TEXTPLUSSTUFF_STUFFGROUPS = {
    'stacks': {
        'name': 'Stacks Modules',
        'description': "Aggregates all Stacks Stuff."
    },
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'stacks_contentgroup': [
        ('square_crop', 'crop__490x490')
    ]
}
