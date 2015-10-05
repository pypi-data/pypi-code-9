from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

from django.conf import settings

import pytz
import datetime

from django.contrib.auth import get_user_model
User = get_user_model()

class CustomAuthenticationBackend(object):

    def authenticate(self, username=None, email=None, password=None):
        try:
            user = None
            if not username:
                user = User.objects.get(email=email)
            else:
                user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid credential!')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('This user was deleted!')

        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        token_lifetime = token.created + datetime.timedelta(hours=settings.EXPIRATION_TIME)
        if token_lifetime < utc_now:
            raise exceptions.AuthenticationFailed('Token has expired!')

        return token.user, token
