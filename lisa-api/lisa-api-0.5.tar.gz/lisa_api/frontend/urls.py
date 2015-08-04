from django.conf.urls import url
from django.shortcuts import HttpResponseRedirect
from . import views as frontend_views
from django.contrib.auth import views as auth_views

template_name = {'template_name': 'login.html'}

urlpatterns = [
    url(r'^$', lambda x: HttpResponseRedirect('/dashboard/')),
    url(r'^dashboard/$', frontend_views.dashboard, name='dashboard'),
    url(r'^plugins/$', frontend_views.plugins, name='plugins'),
    url(r'^ajax/plugins/changelog/(?P<plugin_name>\w+)$', frontend_views.plugin_changelog, name='changelog'),
    url(r'^login/$', auth_views.login, template_name, name='login'),
    url(r'^logout/$', auth_views.logout, template_name, name='logout'),
]
