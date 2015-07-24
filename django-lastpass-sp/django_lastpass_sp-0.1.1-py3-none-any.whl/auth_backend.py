from django.conf import settings
from django.contrib.auth.models import User


class SAMLServiceProviderBackend(object):

    def authenticate(self, saml_authentication=None):
        if not saml_authentication:  # Using another authentication method
            return None

        if saml_authentication.is_authenticated():
            attributes = saml_authentication.get_attributes()
            print dir(saml_authentication)
            print attributes
            try:
                email = saml_authentication.get_nameid()
                user = User.objects.get(username=email.split('@')[0])
            except User.DoesNotExist:
                superuser = getattr(settings, 'LASTPASS_CREATE_ADMIN', False)
                staff = getattr(settings, 'LASTPASS_CREATE_STAFF', False)
                user = User(username=email.split('@')[0], email=email,
                            is_superuser=superuser, is_staff=staff)
                user.set_unusable_password()
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
