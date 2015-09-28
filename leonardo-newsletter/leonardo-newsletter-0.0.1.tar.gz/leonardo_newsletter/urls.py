from django.conf.urls import url, include, patterns

urlpatterns = patterns('',
                       url(r'^tracking/', include('emencia.django.newsletter.urls.tracking')),
                       url(r'^statistics/', include('emencia.django.newsletter.urls.statistics')),
                       )
