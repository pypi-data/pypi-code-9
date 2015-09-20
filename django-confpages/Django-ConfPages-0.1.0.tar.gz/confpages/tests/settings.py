SECRET_KEY = 'your-own-secret-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
   }
}

INSTALLED_APPS = (
    'confpages',
)

ROOT_URLCONF = 'confpages.tests.urls'
