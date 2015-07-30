from django.conf import settings


STYLES = getattr(
    settings, 'CALLTOACTION_STYLES',
    (('calltoaction/default.html', 'default'), )
)
