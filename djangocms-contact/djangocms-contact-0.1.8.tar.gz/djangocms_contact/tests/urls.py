from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact/', include('djangocms_contact.urls',
                              namespace='djangocms_contact')),
    url(r'', include('cms.urls')),
]
