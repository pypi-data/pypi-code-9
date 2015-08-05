from django.conf.urls import patterns, include, url
from scroller.views import ImageView, SampleView
#from django.contrib import admin
from .settings import STATIC_ROOT
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'image_viewer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^static/(.*)$', 'django.views.static.serve',
        {'document_root': STATIC_ROOT, 'show_indexes' : True}),
    url(r'^home/$', ImageView.as_view(), name='image-view'),
    url(r'^/$', SampleView.as_view(), name='demo'),
)
