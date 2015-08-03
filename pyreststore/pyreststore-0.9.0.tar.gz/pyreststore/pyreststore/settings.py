# -*- coding: utf-8; mode: Python; -*-
'''
Django settings for pyreststore project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
'''

try:
    from settings_dev import *
except ImportError:
    pass

try:
    from settings_local import *
except ImportError:
    pass
