from django.conf.urls import url
from pages import views

pages = [
    url(r'^(?P<path0>[a-z0-9_\-/]+)/$', views.DefaultHtmlView.as_view(), name='pages'),
]

root = [
    url(r'^sitemap\.xml$', views.SiteMapXmlView.as_view(), name='sitemap'),
]
