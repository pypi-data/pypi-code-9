# These settings override the default settings

# The geonode location.
SITEURL = 'http://192.168.99.100/'
DEBUG = True

ALLOWED_HOSTS = (
'192.168.99.100',
'localhost',
'192.168.99.100',
)

PROXY_ALLOWED_HOSTS = (
'*',
'192.168.99.100',
'.lmnsolutions.com',
'.openstreetmap.org',
)

ADMINS = (
('ROGUE', 'ROGUE@lmnsolutions.com'),
)

CLASSIFICATION_BANNER_ENABLED = False




SERVER_EMAIL = 'ROGUE@192.168.99.100'
DEFAULT_FROM_EMAIL = 'webmaster@192.168.99.100'
REGISTRATION_OPEN = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'geonode',
        'USER': 'geonode',
        'PASSWORD': 'geonode',
        'HOST': 'rogue-database',
        'PORT': '5432',
    },

    'geonode_imports': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geonode_imports',
        'USER': 'geonode',
        'PASSWORD': 'geonode',
        'HOST': 'rogue-database',
        'PORT': '5432',
    },
}

# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default': {
        'BACKEND': 'geonode.geoserver',
        'LOCATION': 'http://192.168.99.100/geoserver/',
        'PUBLIC_LOCATION': 'http://192.168.99.100/geoserver/',
        'USER': 'admin',
        'PASSWORD': 'geoserver',
        'MAPFISH_PRINT_ENABLED': True,
        'PRINT_NG_ENABLED': True,
        'GEONODE_SECURITY_ENABLED': True,
        'GEOGIG_ENABLED': True,
        'WMST_ENABLED': False,
        'DATASTORE': 'geonode_imports',
        'GEOGIG_DATASTORE_DIR':'/var/lib/geoserver_data/geogig',
        }
    }

#  Database datastore connection settings
GEOGIG_DATASTORE_NAME = 'geogig-repo'


UPLOADER = {
    'BACKEND' : 'geonode.importer',
    'OPTIONS' : {
        'TIME_ENABLED' : True,
        'GEOGIG_ENABLED' : True,
    }
}

STATIC_ROOT = '/var/www/rogue'
MEDIA_ROOT = '/var/www/rogue/media'

# CSW settings
CATALOGUE = {
    'default': {
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        'URL': '%scatalogue/csw' % SITEURL,
    }
}


BROKER_URL = 'amqp://geoshape:geoshape@127.0.0.1:5672'
CELERY_ALWAYS_EAGER = False
NOTIFICATION_QUEUE_ALL = not CELERY_ALWAYS_EAGER

