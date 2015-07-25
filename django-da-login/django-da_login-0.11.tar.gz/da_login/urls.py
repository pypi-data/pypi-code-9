# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.core.urlresolvers import reverse
# from oscar.app import application
# Uncomment the next two lines to enable the admin:

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from django.contrib import admin
from django.views.generic import TemplateView
from da_login.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       # url(r'^login$', 'da_login.views.login', name='login'),
                       url(r'^login', LoginView.as_view(), name='login'),
                       url(r'^register$', RegisterView.as_view(), name='register'),

                       url(r'^profile$', 'da_login.views.profile', name='profile'),

                       url(r'^logout$', 'da_login.views.logout', name='logout'),
                       #
                       url(r'^edit_profile$', 'da_login.views.edit_profile', name='edit_profile'),
                       # url(r'^profile_change_avatar$', 'da_login.views.profile_change_avatar', name='profile_change_avatar'),
                       #
                       # url(r'^profile/(?P<username>[a-zA-Z0-9\-_\.\/]+)$', 'da_login.views.another_profile', name='another_profile'),

                       # url(r'^node_subscribe$', 'da_login.views.node_subscribe', name='node_subscribe'),
                       )
