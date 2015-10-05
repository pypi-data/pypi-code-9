from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login/$', views.CustomAuthTokenView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutAuthTokenView.as_view(), name='logout'),
    url(r'^signup/$', views.sign_up, name='signup')
]
