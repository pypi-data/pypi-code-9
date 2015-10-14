from django.conf.urls import patterns, url

from changer.c5.filebrowser.settings import UPLOAD_FRONTEND

urlpatterns = patterns('',    
    url(r'^upload/', 'changer.c5.filebrowser.upload_frontends.%s.views.upload' % UPLOAD_FRONTEND, name="fb_upload"),
    url(r'^check_file/$', 'changer.c5.filebrowser.upload_frontends.%s.views._check_file' % UPLOAD_FRONTEND, name="fb_check"),
    url(r'^upload_file/$', 'changer.c5.filebrowser.upload_frontends.%s.views._upload_file' % UPLOAD_FRONTEND, name="fb_do_upload"),
)
