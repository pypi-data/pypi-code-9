__author__ = 'xueqing'
from django.conf.urls import patterns,url
from bases import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
)