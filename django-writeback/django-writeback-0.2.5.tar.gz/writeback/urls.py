# -*- coding: utf-8 -*-

from django.conf.urls import *

from .views import MessageCreateView


urlpatterns = patterns('',

    url(r'^$', MessageCreateView.as_view(), name='writeback_message_create'),

)
