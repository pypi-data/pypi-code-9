from __future__ import with_statement

from django.conf.urls import patterns, url

from . import views

urlpatterns = [
    url(r'^(?P<otp_key>\w+)/$', views.otl_view, name='one-time-link'),
]
