from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^upload_pic/$', views.upload_pic, name='upload_pic'),
    url(r'^crop_pic/$', views.crop_pic, name='crop_pic'),
)
