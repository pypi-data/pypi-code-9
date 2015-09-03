
from django.conf.urls import include, patterns, url

urlpatterns = patterns('',
                       url(r'^admin/rosetta/', include('rosetta.urls')),
                       )
