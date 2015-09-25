try:
    from wagtail.tests.settings import *
except ImportError:
    pass

INSTALLED_APPS += (
    'wagtailplus.wagtaillinks.apps.WagtailLinksAppConfig',
    'wagtailplus.wagtailrelations.apps.WagtailRelationsAppConfig',
    'wagtailplus.wagtailrollbacks.apps.WagtailRollbacksAppConfig',
)