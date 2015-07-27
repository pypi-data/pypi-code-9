import os.path
from geokey.core.settings.dev import *

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DEFAULT_FROM_EMAIL = 'sender@example.com'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'geokey',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'django',
        'PASSWORD': 'django123',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

ENABLE_VIDEO = True
YOUTUBE_AUTH_EMAIL = 'your-email@example.com'
YOUTUBE_AUTH_PASSWORD = 'password'
YOUTUBE_DEVELOPER_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
YOUTUBE_CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com'

INSTALLED_APPS += (
    'geokey_epicollect',
    # 'geokey_cartodb',
    'geokey_communitymaps',
    'geokey_sapelli',
    'geokey_export',
    'geokey_geotagx',
    'pantechnicon',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = normpath(join(dirname(dirname(abspath(__file__))), 'assets'))
MEDIA_URL = '/assets/'

WSGI_APPLICATION = 'local_settings.wsgi.application'

if os.path.exists('local_settings/urls.py'):
    ROOT_URLCONF = 'local_settings.urls'
else:
    ROOT_URLCONF = 'geokey.core.urls'

def show_toolbar(request):
    print 'blah'
    return True
SHOW_TOOLBAR_CALLBACK = show_toolbar

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'NOTSET',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         '': {
#             'handlers': ['console'],
#             'level': 'NOTSET',
#         },
#         'django.request': {
#             'handlers': ['console'],
#             'propagate': False,
#             'level': 'ERROR'
#         }
#     }
# }
