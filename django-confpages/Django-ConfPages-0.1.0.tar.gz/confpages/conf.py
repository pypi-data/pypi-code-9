from django.conf import settings as django_settings
from easyconfig import Config

default_settings = {
    'PAGE_LOADER': 'confpages.loaders.DefaultLoader',
    'TOKEN_EXPIRES': 600  # in seconds
}
settings = Config(default_settings)

# Get the global settings for the confpages app
global_settings = getattr(django_settings, 'CONFPAGES', {})

# Validate the global settings
assert isinstance(global_settings, dict), \
    'The `CONFPAGES` setting must be a dictionary'

difference = set(global_settings.keys()) - set(default_settings.keys())
assert not len(difference), ('The keys %r in the `CONFPAGES` setting are '
                             'not supported' % tuple(difference))

# Override the default settings by global ones
settings.from_mapping(global_settings)
