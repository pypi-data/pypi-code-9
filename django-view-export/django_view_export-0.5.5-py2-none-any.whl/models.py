from django.conf import settings
from django.db import models

# Default settings: You may override these in a project settings dictionary
# called VIEW_EXPORT_CONFIG.
config = {
    'OFF_PEAK_VIEWS': [],
}
config.update(getattr(settings, 'VIEW_EXPORT_CONFIG', {}))
