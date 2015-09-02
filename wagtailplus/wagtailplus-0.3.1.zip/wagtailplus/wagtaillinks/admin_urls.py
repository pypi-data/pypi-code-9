"""
Contains application administration URLs.
"""
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from wagtailplus.utils.views import crud

from .models import Link
from .views import chooser
from .views import links

urlpatterns = [
    # CRUD URLs.
    url(
        r'^$',
        crud.IndexView.as_view(
            model           = Link,
            template_dir    = 'wagtaillinks/links'
        ),
        name='index'
    ),
    url(
        r'^add/$',
        permission_required('wagtaillinks.add_link')(links.CreateView.as_view(
            model           = Link,
            url_namespace   = 'wagtaillinks',
            template_dir    = 'wagtaillinks/links'
        )),
        name='add'
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        permission_required('wagtaillinks.change_link')(links.UpdateView.as_view(
            model           = Link,
            url_namespace   = 'wagtaillinks',
            template_dir    = 'wagtaillinks/links'
        )),
        name='edit'
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        permission_required('wagtaillinks.delete_link')(crud.DeleteView.as_view(
            model           = Link,
            url_namespace   = 'wagtaillinks',
            template_dir    = 'wagtaillinks/links'
        )),
        name = 'delete'
    ),
    # Chooser URLs.
    url(
        r'^chooser/(?P<pk>\d+)/$',
        chooser.LinkChosen.as_view(
            model           = Link,
            url_namespace   = 'wagtaillinks',
            template_dir    = 'wagtaillinks/chooser'
        ),
        name = 'chosen'
    ),
]
