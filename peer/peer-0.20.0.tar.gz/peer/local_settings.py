
# local settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  # ('Your Name', 'your_email@example.com'),
)

ALLOWED_HOSTS = ['localhost', 'peer']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',      # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/data/peer.db',                     # Or path to database file if using sqlite3.
    }
}

TIME_ZONE = 'Europe/Madrid'

RECAPTCHA_PUBLIC_KEY = 'B3f9AMzXIRKf4g3P+i6DdlhEwPDktpwPXgIWIU84'
RECAPTCHA_PRIVATE_KEY = 'znBQ2p15czPwqtfc0INtZu9TJtc8Ya1ukwfhXAh3'

SAML_ENABLED = False
SAML_CONFIG = {}
REMOTE_USER_ENABLED = False

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
