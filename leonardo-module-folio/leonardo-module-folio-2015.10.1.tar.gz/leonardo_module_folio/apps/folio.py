from django.conf.urls import url, patterns


urlpatterns = patterns('leonardo_module_folio.views',
                       url(r'^$', 'project_list', {}, 'folio_project_list'),
                       url(r'^(?P<project_slug>[0-9a-z\-]+)/$',
                           'project_detail', {}, 'folio_project_detail'),
                       )
