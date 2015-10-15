__author__ = 'vinay'
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^cms/ajax/save/(?P<save_type>.+)/$',
        views.save, name='save_cms_content'),
]
