from saml_service_provider.settings import SAMLServiceProviderSettings


class LastPassServiceProviderSettings(SAMLServiceProviderSettings):
    def __init__(self, onelogin_connector_id, onelogin_x509_cert=None,
                 onelogin_x509_fingerprint=None, **kwargs):
        self.contact_info = {
            "technical": {
                "givenName": "Admin",
                "emailAddress": kwargs.get('SAML_SP_ADMIN_EMAIL',
                                           'admin@example.com')
            }
        }

        if 'contact_info' in kwargs:
            self.contact_info = kwargs.pop('contact_info')

        if 'organization_info' in kwargs:
            self.organization_info = kwargs.pop('organization_info')

        conf = dict()
        conf['idp_metadata_url'] = 'https://lastpass.com/saml/login/{}'.format(
            onelogin_connector_id
        )
        conf['idp_sso_url'] = 'https://lastpass.com/saml/login/{}'.format(
            onelogin_connector_id
        )
        conf['idp_slo_url'] = 'https://lastpass.com/saml/logout/{}'.format(
            onelogin_connector_id
        )
        if onelogin_x509_cert:
            conf['idp_x509cert'] = onelogin_x509_cert
        elif onelogin_x509_fingerprint:
            conf['idp_x509_fingerprint'] = onelogin_x509_fingerprint
        else:
            raise Exception('Provide either cert or fingerprint')

        kwargs.update(conf)
        super(LastPassServiceProviderSettings, self).__init__(**kwargs)
        self.settings['sp']['NameIDFormat'] = "urn:oasis:names:tc:SAML:2.0:name-id-format:emailAddress"
