from django.conf.urls import include, url
from .views import download_file

urlpatterns = [

    url(r'^/download/(?P<file_id>[0-9]+)/$', download_file, name='download_file'),
]
