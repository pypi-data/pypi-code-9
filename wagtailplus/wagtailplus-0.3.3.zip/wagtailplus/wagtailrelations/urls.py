"""
Contains application URLs.
"""
from django.conf.urls import url

from .views import (
    CategoriesView,
    EntriesView
)


urlpatterns = [
    url(r'^$', CategoriesView.as_view(), name='site_map'),
    url(r'^(?P<slug>[\w-]+)/$', EntriesView.as_view(), name='entries_list'),
]
