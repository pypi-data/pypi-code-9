from django.conf import settings
from django.utils.translation import ugettext_lazy as _

SIMPLEPROFILE_PROFILE_UPDATED = getattr(settings,
    'SIMPLEPROFILE_PROFILE_UPDATED',
    _(u'Your profile has been updated'))
