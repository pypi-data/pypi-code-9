from django.conf.urls.defaults import *

from changer.c5.rating.views import rate

urlpatterns = patterns('',
    (r'^rate/$', rate),
)
