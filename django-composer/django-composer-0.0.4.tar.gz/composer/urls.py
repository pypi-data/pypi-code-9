"""
urls.py
"""
from django.conf.urls import patterns, url
from django.conf import settings

from .views import EditComposerElementView, ExampleView


urlpatterns = patterns(
    '',

    url(r'edit/(?P<pk>[\d]+)$', EditComposerElementView.as_view(), name='composer-edit-element')
)

if settings.DEBUG:
    urlpatterns += (
        url(r'example/', ExampleView.as_view(), name='composer-example'),
    )
