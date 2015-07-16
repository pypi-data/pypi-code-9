"""lisa_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from lisa_api.api import views as api_views
from rest_framework import routers
from lisa_api.lisa.plugin_manager import PluginManager


router = routers.DefaultRouter()
router.register(r'clients', api_views.ClientViewSet)
router.register(r'groups', api_views.GroupViewSet)
router.register(r'intents', api_views.IntentViewSet)
router.register(r'plugins', api_views.PluginViewSet)
router.register(r'users', api_views.UserViewSet)
router.register(r'zones', api_views.ZoneViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include('lisa_api.frontend.urls', namespace='frontend')),
    url(r'^api/v1/core/', include(router.urls)),
    url(r'^api/v1/core/speak/', api_views.SpeakView),
    url(r'^api/v1/core/tts/', api_views.TTSView),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]

for plugin in PluginManager().plugins:
        urlpatterns.append(url(r'^api/v1/plugin-%s' % plugin, include('lisa_plugins_%s.urls' % plugin)))
