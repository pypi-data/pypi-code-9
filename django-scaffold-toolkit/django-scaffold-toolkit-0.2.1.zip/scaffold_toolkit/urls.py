#coding=utf-8
from django.conf.urls import url
from scaffold_toolkit.views import kindeditor_upload_file

urlpatterns = [url(r'^kind_upload/$', kindeditor_upload_file, name='kind_upload'),
               ]
