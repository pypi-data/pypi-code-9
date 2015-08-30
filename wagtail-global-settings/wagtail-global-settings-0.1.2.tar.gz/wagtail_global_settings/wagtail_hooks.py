from __future__ import unicode_literals, absolute_import

from django.conf.urls import include, url
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem, SubmenuMenuItem

from wagtail_global_settings import urls
from wagtail_global_settings.permissions import user_can_edit_global_settings

class GlobalSettingsMenuItem(MenuItem):
    pass

class SiteSettingsMenuItem(MenuItem):
    pass

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^global-settings/', include(urls)),
    ]

@hooks.register('construct_main_menu')
def construct_main_menu(request, menu_items):
    if user_can_edit_global_settings(request.user):
        settings_menu_items = [item for item in menu_items if item.name == 'settings' and isinstance(item, SubmenuMenuItem)]
        if len(settings_menu_items) == 0:
            # settings menu not found
            g_menu_items = menu_items
        else:
            g_menu_items = settings_menu_items[0].menu.registered_menu_items
        
        global_settings_menu_items = [item for item in g_menu_items if item.name == 'global-settings' and isinstance(item, GlobalSettingsMenuItem)]
        if len(global_settings_menu_items) == 0:
            g_menu_items.append(
                GlobalSettingsMenuItem(_('Global settings'), urlresolvers.reverse('wagtail_global_settings_choose'),
                         classnames='icon icon-cog', name='global-settings', order=12000)
            )
        
        site_settings_menu_items = [item for item in g_menu_items if item.name == 'site-settings' and isinstance(item, SiteSettingsMenuItem)]
        if len(site_settings_menu_items) == 0:
            g_menu_items.append(
                SiteSettingsMenuItem(_('Site settings'), urlresolvers.reverse('wagtail_site_settings_choose_site'),
                         classnames='icon icon-cog', name='site-settings', order=10000)
            )
