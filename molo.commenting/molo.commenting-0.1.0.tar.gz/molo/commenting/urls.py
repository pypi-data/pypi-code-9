from django.conf.urls import patterns, include, url

from molo.commenting import views


urlpatterns = patterns(
    '',
    url('report/(\d+)/$', views.report, name='comments-report'),
    url('', include('django_comments.urls')),
)
