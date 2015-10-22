from django.conf.urls import include, patterns, url

from . import views
from luhublog.feed import BlogFeed 

urlpatterns = patterns('',
	url(r'^$', views.EntryListView.as_view(), name='luhublog-list'),
	url(r'^feed/$', BlogFeed(), name='luhublog-feed' ),
	url(r'^(?P<slug>[\w-]+)/$', views.EntryDetailView.as_view(), name='luhublog-detail'),
)