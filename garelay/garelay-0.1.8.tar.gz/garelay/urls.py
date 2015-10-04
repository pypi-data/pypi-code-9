import os

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

if not os.environ.get('GARELAY_NO_TRACKER'):
    urlpatterns += patterns(
        '',
        url(r'^', include('garelay.tracker.urls')),
    )

if not os.environ.get('GARELAY_NO_SERVER'):
    urlpatterns += patterns(
        '',
        url(r'^', include('garelay.server.urls')),
    )

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + 'images/',
        document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
