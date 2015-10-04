from ..settings.base import *


# Disable debug mode

DEBUG = False
TEMPLATE_DEBUG = False

ROOT_URLCONF = 'garelay.tracker.urls'

BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERYBEAT_SCHEDULE = {
    'relay-events': {
        'task': 'garelay.tracker.tasks.relay_events',
        'schedule': timedelta(minutes=1),
    },
}

try:
    from .local import *
except ImportError:
    pass
