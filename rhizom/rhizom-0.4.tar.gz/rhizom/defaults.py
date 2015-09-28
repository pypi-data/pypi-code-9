# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'rhizom.db')
BROWSERID_AUDIENCE = ["http://127.0.0.1:5000", "http://127.0.0.1:5001"]
SECRET_KEY = 'SomethingVerySecretThatYouMustChange'
ADMINS = ("you@example.com")
TEMPLATE_DIRS = []
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # Don't upload more than 16MB

# i18n
BABEL_DEFAULT_LOCALE = "fr"
BABEL_DEFAULT_TIMEZONE = "Europe/Paris"
