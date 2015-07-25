# -*- coding: utf-8 -*-
__author__ = 'hramik'

import logging
from django.conf import settings
from django.contrib.sites.models import get_current_site
from da_login.forms import *


def login_context_processor(request):
    current_ip = request.META['REMOTE_ADDR']
    user = request.user

    if "user" in request.session:
        user_cookie = request.session["user"]
    else:
        request.session["user"] = 'test'
        user_cookie = request.session["user"]

    # Login Forms
    login_form = LoginForm(initial={
        'username': '',
        'password': '',
    })

    register_form = RegisterForm(initial={
        'username': '',
        'password': '',
    })

    userprofile = None
    if request.user.is_authenticated():
        userprofile = request.user.userprofile


    return {
        'path': request.path,
        'user': user,
        'login_form': login_form,
        'register_form': register_form,
        'request': request,
        'userprofile': userprofile,
    }
