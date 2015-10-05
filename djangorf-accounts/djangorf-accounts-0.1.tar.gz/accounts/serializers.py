from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model, authenticate
User = get_user_model()

UNAUTHORIZED_MESSAGE = 'Unable to log with provided credentials.'

class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        data={
            'username': attrs.get('username'),
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = None
        if (data['username'] or data['email']) and data['password']:
            user = authenticate(**data)

            if not user:
                msg = _(UNAUTHORIZED_MESSAGE)
                raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs
