try:
    from django.conf.urls import url, patterns
except ImportError:
    from django.conf.urls.defaults import url, patterns

from redactor.views import DefaultRedactorUploadView
from redactor.forms import FileForm


urlpatterns = patterns(
    '',
    url(
        '^upload/image/(?P<upload_to>.*)',
        DefaultRedactorUploadView.as_view(),
        name='redactor_upload_image'),
    url(
        '^upload/file/(?P<upload_to>.*)',
        DefaultRedactorUploadView.as_view(),
        {'form_class': FileForm},
        name='redactor_upload_file'))
