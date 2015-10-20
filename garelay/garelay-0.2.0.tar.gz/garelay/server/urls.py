from django.conf.urls import patterns, url

from .views import server


urlpatterns = patterns(
    '',
    url(r'^server/', server, name='server'),
)
