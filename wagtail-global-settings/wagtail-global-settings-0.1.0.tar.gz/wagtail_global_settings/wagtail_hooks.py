from __future__ import unicode_literals, absolute_import

from django.conf.urls import include, url
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem

from . import urls
from .permissions import user_can_edit_global_settings

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^global-settings/', include(urls)),
    ]

@hooks.register('construct_main_menu')
def construct_main_menu(request, menu_items):
    if user_can_edit_global_settings(request.user):
        menu_items.append(
            MenuItem(_('Global settings'), urlresolvers.reverse('wagtail_global_settings_choose'),
                     classnames='icon icon-cogs', order=10000)
        )