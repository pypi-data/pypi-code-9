from views import ControllerViewSet
from rest_framework import routers
from django.conf.urls import include, url

router = routers.DefaultRouter()
router.register(r'controllers', ControllerViewSet)

urlpatterns = [
    url(r'^/', include(router.urls)),
]
