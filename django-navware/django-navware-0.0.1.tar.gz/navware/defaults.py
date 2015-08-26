from django.conf import settings

# Should NavWare autoload its template tags
NAVWARE_AUTOLOAD_TEMPLATE_TAGS = getattr(settings, 'NAVWARE_AUTOLOAD_TEMPLATE_TAGS', True)
