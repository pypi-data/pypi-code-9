from django.conf.urls import patterns, include, url

from molo.commenting import views


urlpatterns = patterns(
    '',
    url(r'molo/report/(\d+)/$', views.report, name='molo-comments-report'),
    url(r'molo/post/$', views.post_molo_comment, name='molo-comments-post'),
    url(r'', include('django_comments.urls')),
)
