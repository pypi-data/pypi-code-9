# -*- encoding:utf-8 -*-
from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
                       url(r'^site-disabled/(?P<ip_address>.*)/(?P<country_code>[\w]+)/$',
                           views.DisabledView.as_view(), name='ipapi-disabled'))
