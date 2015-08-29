from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from .views import choose, edit


urlpatterns = [
    url(r'^$', choose, name='wagtail_global_settings_choose'),
    url(r'^(?P<pk>\d+)/$', edit, name='wagtail_global_settings_edit'),
]
