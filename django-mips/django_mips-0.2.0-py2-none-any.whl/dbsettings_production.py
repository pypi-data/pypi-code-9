"""
Database settings with real values.  Not for public VCS use!

"""

# import os
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DBNAME = 'newtbase'
USER = 'newtbase'
PASSWORD = '3805dacc893745f4a5b33da33e77fcac'
HOST = '149.156.165.104'

# DBNAME = 'newtbase'
# USER = 'molecol'
# PASSWORD = 'fefb9f36eff3c2e8b6fbc04b26986f4f'
# HOST = '149.156.165.104'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '05u6ysw7e8(gnhnu9i3s$_b(kkw_5g)g91c!=hv#x5c0isw*)='

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DBNAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST
    }
}