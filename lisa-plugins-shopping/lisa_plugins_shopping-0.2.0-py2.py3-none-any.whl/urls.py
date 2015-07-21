from lisa_plugins_shopping.views import ShoppingListViewSet
from rest_framework import routers
from django.conf.urls import include, url

router = routers.DefaultRouter()
router.register(r'lists', ShoppingListViewSet)

urlpatterns = [
    url(r'^/', include(router.urls)),
]
