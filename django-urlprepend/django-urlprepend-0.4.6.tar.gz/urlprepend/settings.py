import re
from django.conf import settings

assert not ( hasattr(settings, 'PREPEND_STRING') and hasattr(settings, 'PREPEND_STRINGS') ), "Cannot have both PREPEND_STRING and PREPEND_STRINGS settings. Pick one"
if hasattr(settings, 'PREPEND_STRINGS'):
    PREPEND_STRINGS = settings.PREPEND_STRINGS
    PATH_RE = re.compile(r'^/(?P<prepend>%s)(?P<path>.*)$' % ('|'.join(PREPEND_STRINGS)))
else:
    PREPEND_STRING = getattr(settings, 'PREPEND_STRING', 'i')
    PATH_RE = re.compile(r'^/(?P<prepend>%s)(?P<path>.*)$' % PREPEND_STRING)



PREPEND_INDEPENDENT_PATHS = getattr(settings, 'PREPEND_INDEPENDENT_PATHS', (re.compile('^/favicon\.ico$'),re.compile('^/sitemap\.xml$'),re.compile('^/media/.*?'),re.compile('^/api/.*?'),re.compile('^/tagging_autocomplete/.*?'),))

PREPEND_INDEPENDENT_MEDIA_URL = getattr(settings, 'PREPEND_INDEPENDENT_MEDIA_URL', True)

PREPEND_TARGET_ATTRIBUTES_TO_IGNORE = getattr(settings, 'PREPEND_TARGET_ATTRIBUTES_TO_IGNORE', ['_parent', '_blank'])