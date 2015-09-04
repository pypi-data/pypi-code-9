from django.conf.urls.static import static
from django.conf.urls import patterns, url, include


from .views import *

urlpatterns = patterns('',
    
    url(r'^track/img\.jpeg$', TrackView.as_view(), name="track_image_view"),
)
