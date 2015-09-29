# -*- coding:utf-8 -*-
from django.contrib.auth import get_user_model


def user_exists(email):
    model = get_user_model()
    return bool(model.objects.filter(email=email).exists())