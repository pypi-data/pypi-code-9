from ..settings.base import *


# Disable debug mode

DEBUG = False
TEMPLATE_DEBUG = False


ROOT_URLCONF = 'garelay.server.urls'

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULE = {
    'register-events': {
        'task': 'garelay.server.tasks.register_events',
        'schedule': timedelta(minutes=1),
    },
}

try:
    from .local import *
except ImportError:
    pass
