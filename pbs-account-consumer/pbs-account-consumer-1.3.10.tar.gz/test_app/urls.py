from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^djadmin/', include(admin.site.urls)),
    url(r'^openid/', include('pbs_account_consumer.urls')),
]
