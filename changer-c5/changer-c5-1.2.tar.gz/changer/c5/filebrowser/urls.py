from django.conf.urls import url, patterns, include

from .settings import UPLOAD_FRONTEND

urlpatterns = patterns('',
    # filebrowser urls
    url(r'^browse/$', 'changer.c5.filebrowser.views.browse', name="fb_browse"),
    url(r'^mkdir/', 'changer.c5.filebrowser.views.mkdir', name="fb_mkdir"),
    url(r'^rename/$', 'changer.c5.filebrowser.views.rename', name="fb_rename"),
    url(r'^delete/$', 'changer.c5.filebrowser.views.delete', name="fb_delete"),
    url(r'^versions/$', 'changer.c5.filebrowser.views.versions', name="fb_versions"),
    (r'^', include('changer.c5.filebrowser.upload_frontends.%s.urls' % UPLOAD_FRONTEND)),
)