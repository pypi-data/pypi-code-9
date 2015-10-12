
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

default_app_config = 'leonardo_admin_sso.Config'

LEONARDO_OPTGROUP = 'Admin SSO'
LEONARDO_APPS = ['leonardo_admin_sso', 'admin_sso']

LEONARDO_AUTH_BACKENDS = [
    'admin_sso.auth.DjangoSSOAuthBackend',
]

LEONARDO_CONFIG = {
    'DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID': ('8082..', _(
        'OAuth Client ID')),
    'DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET': ('secret', _(
        'OAuth Client Secret')),
    'DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON': (True, _(
        'Show Login Button for SSO'))
}


class Config(AppConfig):
    name = 'leonardo_admin_sso'
    verbose_name = "leonardo-admin-sso"

    def ready(self):

        import leonardo.site
        leonardo.site.leonardo_admin.login_template = 'admin_sso/login.html'

        # monkey patch settings
        from django.conf import settings as django_settings
        from admin_sso import settings
        for key in list(LEONARDO_CONFIG.keys()):
            setattr(settings, key, getattr(django_settings, key, None))
