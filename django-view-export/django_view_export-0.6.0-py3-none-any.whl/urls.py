from django.conf.urls import patterns, url

urlpatterns = patterns(
    'view_export.views',
    url(r'^view-export/(?P<view>.+)/$', 'csv_view_export'),
)
