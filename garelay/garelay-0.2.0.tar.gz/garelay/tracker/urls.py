from django.conf.urls import patterns, url

from .views import tracker


urlpatterns = patterns(
    '',
    url(r'^(?P<path>.*)/tracker-(?P<tracking_id>[A-Za-z0-9\-]+)\.gif',
        tracker, name='tracker'),
)
