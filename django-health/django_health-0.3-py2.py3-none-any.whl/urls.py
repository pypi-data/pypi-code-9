from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.HealthView.as_view(), name='health'),
    url(r'cache/$', views.CacheHealthView.as_view(), name='health-cache'),
    url(r'db/$', views.DBHealthView.as_view(), name='health-db'),
]
