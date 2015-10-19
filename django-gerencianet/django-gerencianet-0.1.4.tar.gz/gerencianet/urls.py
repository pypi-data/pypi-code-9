#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'gerencianet.views',
    url(r'^getpaymentlink/$', 'get_payment_link_view', name='get_payment_link'),
    url(r'^getnotificationinfo/$', 'get_notification_info_view', name='get_notification_info'),
)