# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from private_messages.views import (InboxView, OutboxView, MessageView, SendMessageView, DeleteMessageView,
                                    ReceiversSelect2View)

urlpatterns = [
    url(r'^inbox/$', InboxView.as_view(), name='inbox'),
    url(r'^outbox/$', OutboxView.as_view(), name='outbox'),
    url(r'^message/(?P<pk>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12})/$',
        MessageView.as_view(), name='read_message'),
    url(r'^message/(?P<pk>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12})/delete/$',
        DeleteMessageView.as_view(), name='delete_message'),
    url(r'^new/$', SendMessageView.as_view(), name='send_message'),
    url(r'^select2/$', ReceiversSelect2View.as_view(), name='select2')
]
