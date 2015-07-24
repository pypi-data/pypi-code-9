from django.conf import settings
from django.core.urlresolvers import reverse

from saml_service_provider import views as samlviews
from .settings import LastPassServiceProviderSettings


class SettingsMixin(object):
    def get_onelogin_settings(self):
        conf = dict()
        conf['onelogin_connector_id'] = settings.LASTPASS_CONNECTOR_ID
        if hasattr(settings, 'LASTPASS_CERTIFICATE'):
            conf['onelogin_x509_cert'] = settings.LASTPASS_CERTIFICATE
        elif hasattr(settings, 'LASTPASS_CERTIFICATE_FILE'):
            with open(settings.LASTPASS_CERTIFICATE_FILE, 'rb') as cert:
                conf['onelogin_x509_cert'] = cert.read()
        else:
            conf['onelogin_x509_fingerprint'] = settings.LASTPASS_FINGERPRINT

        hostname = getattr(settings, 'LASTPASS_HOSTNAME', 'http://localhost:8000')

        conf['sp_metadata_url'] = hostname + reverse('saml_metadata')
        conf['sp_login_url'] = hostname + reverse('saml_login_complete')
        conf['sp_logout_url'] = hostname + reverse('logout')
        conf['debug'] = settings.DEBUG
        conf['strict'] = not settings.DEBUG

        if hasattr(settings, 'SAML_SP_CERTIFICATE'):
            conf['sp_x509cert'] = settings.SAML_SP_CERTIFICATE
        else:
            with open(settings.SAML_SP_CERTIFICATE_FILE, 'rb') as cert:
                conf['sp_x509cert'] = cert.read()

        if hasattr(settings, 'SAML_SP_KEY'):
            conf['sp_private_key'] = settings.SAML_SP_KEY
        else:
            with open(settings.SAML_SP_KEY_FILE, 'rb') as key:
                conf['sp_private_key'] = key.read()

        if hasattr(settings, 'SAML_SP_CONTACT_INFO'):
            conf['contact_info'] = settings.SAML_SP_CONTACT_INFO

        if hasattr(settings, 'SAML_SP_ORGANIZATION_INFO'):
            conf['organization_info'] = settings.SAML_SP_ORGANIZATION_INFO

        return LastPassServiceProviderSettings(**conf).settings


class InitiateAuthenticationView(SettingsMixin,
                                 samlviews.InitiateAuthenticationView):
    pass


class CompleteAuthenticationView(SettingsMixin,
                                 samlviews.CompleteAuthenticationView):
    pass


class MetadataView(SettingsMixin,
                   samlviews.MetadataView):
    pass
