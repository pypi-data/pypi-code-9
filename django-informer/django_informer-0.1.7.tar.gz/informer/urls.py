# coding: utf-8

"""informer URL configuration"""

from django.conf import settings
from django.conf.urls import url, patterns

from informer.views import DefaultView, InformerDiscoverView
from informer.views import InformerView


API = InformerView.as_view()

DJANGO_INFORMERS = getattr(settings, 'DJANGO_INFORMERS', ())

urlpatterns = patterns(
    '',
    url(r'^$', DefaultView.as_view(), name='default-informer'),
    url(r'^discover/$', InformerDiscoverView.as_view(),
        name='discover-informer'),
)

for namespace, classname in DJANGO_INFORMERS:
    data = {'namespace': namespace, 'classname': classname}
    informer = classname.replace('Informer', '').lower()
    name = 'informer-%s' % informer

    urlpatterns += patterns(
        '',
        url(r'^%s/$' % informer, API, data, name=name),
    )
