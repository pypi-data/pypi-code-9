# -*- coding:utf-8 -*-
from django.contrib.auth import get_user_model


class EmailUserBackend(object):
    def authenticate(self, email=None, password=None):
        model = get_user_model()
        try:
            user = model.objects.filter(email=email).first()
        except model.DoesNotExist as e:
            return None

        if not user:
            return None

        if not user.check_password(password):
            return None

        user.backend = "%s.%s" % (self.__module__, self.__class__.__name__)
        return user

    def get_user(self, user_id):
        model = get_user_model()
        try:
            user = get_user_model().objects.get(id=user_id)
        except model.DoesNotExist:
            return None
        return user
