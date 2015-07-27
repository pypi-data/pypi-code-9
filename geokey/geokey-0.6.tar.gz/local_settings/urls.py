from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^', include('geokey.core.urls')),
    url(r'^', include('geokey_epicollect.urls', namespace='geokey_epicollect')),
    # url(r'^', include('geokey_cartodb.urls', namespace='geokey_cartodb')),
    url(r'^', include('geokey_communitymaps.urls', namespace='community_maps')),
    url(r'^', include('geokey_sapelli.urls', namespace='geokey_sapelli')),
    url(r'^', include('geokey_export.urls', namespace='geokey_export')),
    url(r'^', include('geokey_geotagx.urls', namespace='geokey_geotagx')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
