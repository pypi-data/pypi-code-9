from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from wagtail_global_settings.views import global_settings, site_settings 


urlpatterns = [
    url(r'^global/$', global_settings.choose, name='wagtail_global_settings_choose'),
    url(r'^global/(?P<pk>\d+)/$', global_settings.edit, name='wagtail_global_settings_edit'),
    url(r'^site/$', site_settings.choose_site, name='wagtail_site_settings_choose_site'),
    url(r'^site/(?P<pk>\d+)/$', site_settings.choose, name='wagtail_site_settings_choose'),
    url(r'^site/(?P<pk>\d+)/(?P<ct_pk>\d+)$', site_settings.edit, name='wagtail_site_settings_edit'),
]
