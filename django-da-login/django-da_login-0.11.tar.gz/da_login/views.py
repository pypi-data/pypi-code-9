# -*- coding: utf-8 -*-

import os
import re

from django.db import models
from django.db.models import Q, F
import operator

from django.utils.html import strip_tags

from django.core.cache import cache
from django.views.decorators.cache import cache_page

from django.db import transaction

# from xml.etree import ElementTree
from xml.dom import minidom

from django.shortcuts import get_object_or_404

from django.contrib.sites.models import get_current_site
from django.utils.html import normalize_newlines, linebreaks

import json
from datetime import datetime
import random
from django.contrib.auth.decorators import login_required

from itertools import chain
# from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string

from django.contrib.sites.models import get_current_site
from django.core.files import File
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.db.models import Max
from django.db.models import F, Q

from pprint import pprint
import logging
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic import DetailView, TemplateView, ListView, View
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

import json
import urllib
import urllib2
from urlparse import urlparse
from django.core.files import File
from django.core.files.base import ContentFile

# REST Framework
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from array import *
from django.conf import settings

from django.contrib.sites.models import Site

from da_mailer.helper import *
from operator import attrgetter

from da_login.forms import *
from da_login.models import *

PROJECT_DIR = os.path.dirname(__file__)
location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', x)


def logout(request):
    try:
        auth_logout(request)
    except KeyError:
        pass
    return redirect(request.META.get('HTTP_REFERER'))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('da_login:profile'))

        return render_to_response('da_login/pages/login.html', {
        },
                                  context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        try:
            pre_user = User.objects.get(Q(email=request.POST['login']) | Q(username=request.POST['login']))
            user = authenticate(username=pre_user.username, password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    print("User is valid, active and authenticated")
                    auth_login(request, user)
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                print("The username and password were incorrect.")

            # if request.META.get('HTTP_REFERER'):
            #     print request.META.get('HTTP_REFERER')
            #     return redirect(request.META.get('HTTP_REFERER'))
            # else:
            return redirect(reverse('da_login:profile'))
        except Exception, e:
            print Exception, e
            message = {
                'text': 'Неверный логин или пароль. Проверьте и попробуйте еще раз или зарегестрируйтесь.',
                'type': 'negative',
            }
            return render_to_response('da_login/pages/login.html', {
                'message': message,
            },
                                      context_instance=RequestContext(request))


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('da_login/pages/register.html', {
        },
                                  context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        try:
            pre_user = User.objects.get(Q(email=request.POST['email']) | Q(username=request.POST['username']))
            message = {
                'text': 'Есть такой чувак, попробуйте выбрать другой логин и имейл',
                'type': 'negative',
            }
            return render_to_response('da_login/pages/register.html', {
                'message': message,
            },
                                      context_instance=RequestContext(request))
        except:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                                password=request.POST['password'])

                user.save()

                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                auth_login(request, user)

        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request):
    change_user_form = RegisterForm()
    userprofile = None

    if request.method == 'POST':
        try:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    print("User is valid, active and authenticated")
                    auth_login(request, user)
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                print("The username and password were incorrect.")

            if request.META.get('HTTP_REFERER'):
                print request.META.get('HTTP_REFERER')
                return redirect(request.META.get('HTTP_REFERER'))
        except Exception, e:
            print Exception, e

    if request.user.is_authenticated():

        change_user_form = RegisterForm(
            initial={
                'username': request.user.username,
                'email': request.user.email,
                'city': request.user.userprofile.city,
                'phone': request.user.userprofile.phone,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name
            }
        )

    return render_to_response('da_login/pages/profile.html', {
        'change_user_form': change_user_form,
    },
                              context_instance=RequestContext(request))


@login_required
def another_profile(request, username):
    user_profile = UserProfile.objects.get(user__username=username)

    return render_to_response('da_login/pages/another_profile.html', {
        'a_user_profile': user_profile,
    },
                              context_instance=RequestContext(request))


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        if request.POST['password']:
            user.set_password(request.POST['password'])

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']

        user.save()

        # Edit User Profile Fields
        user_profile = user.get_profile()

        user_profile.city = request.POST['city']
        user_profile.phone = request.POST['phone']

        user_profile.save()

    return redirect(request.META.get('HTTP_REFERER'))


def handle_uploaded_file(file, filedest):
    with open(filedest, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


# @csrf_protect
def image_upload(request):
    if request.method == 'POST':
        print location("media/upload_files")
        try:
            os.mkdir(location("media/upload_files"))
        # result=location("media/upload_files")
        except Exception, e:
            result = "dir"

        try:
            # filedest = os.path.abspath(os.path.dirname(__name__))+'/media/upload_files/'+request.FILES['file'].name
            new_image_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + str(random.randint(100, 999)) + \
                             os.path.splitext(request.FILES['file'].name)[1]
            print new_image_name

            filedest = location("media/upload_files/" + new_image_name)
            result_filedest = '/media/upload_files/' + new_image_name
            print filedest
            handle_uploaded_file(request.FILES['file'], filedest)
            result = result_filedest
        except Exception, e:
            # result='file'
            print Exception, e
            pass

    return HttpResponse(result)


@login_required
def profile_change_avatar(request):
    if request.method == 'POST':
        user = request.user
        user_profile = user.get_profile()

        try:
            os.mkdir(location("media/avatars"))
            result = location("media/avatars")
        except Exception, e:
            result = "dir"

        try:
            # filedest = os.path.abspath(os.path.dirname(__name__))+'/media/upload_files/'+request.FILES['file'].name
            new_image_name = str(request.user.id) + '-' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + str(
                random.randint(100, 999)) + os.path.splitext(request.FILES[
                                                                 'file']
                                                             .name)[1]
            print new_image_name

            filedest = location("media/avatars/" + new_image_name)
            result_filedest = '/media/avatars/' + new_image_name
            avatar_dest = 'avatars/' + new_image_name
            handle_uploaded_file(request.FILES['file'], filedest)
            result = result_filedest

            user_profile.avatar = avatar_dest
            user_profile.save()
        except Exception, e:
            # result='file'
            print Exception, e
            pass

    return HttpResponse(result)
