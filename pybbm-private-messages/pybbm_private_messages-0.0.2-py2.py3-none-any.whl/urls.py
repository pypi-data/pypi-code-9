# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from private_messages.views import InboxView, MessageView, SendMessageView


urlpatterns = [
    url(r'^messages/$', InboxView.as_view(), name='inbox'),
    url(r'^messages/(?P<pk>\d+)/$', MessageView.as_view(), name='read_message'),
    url(r'^messages/new/$', SendMessageView.as_view(), name='send_message'),
]
