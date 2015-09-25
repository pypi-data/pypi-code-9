"""
Contains Wagtail CMS integration hooks.
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.html import format_html_join

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailadmin.site_summary import SummaryItem
from wagtail.wagtailcore import hooks

from . import admin_urls
from . import wagtailadmin_urls
from .models import Link
from .rich_text import LinkHandler


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^links/', include(admin_urls, namespace='wagtaillinks')),
        url(r'', include(wagtailadmin_urls))
    ]

@hooks.register('register_admin_menu_item')
def register_locations_menu_item():
  return MenuItem(
      'Links',
      reverse('wagtaillinks:index'),
      classnames    = 'icon icon-link',
      order         = 410
  )

@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'wagtaillinks/js/hallo-plugins/hallo-wagtaillink.js',
    ]

    js_includes = format_html_join(
        '\n',
        '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes + format_html(
        """
        <script>
            window.chooserUrls.EmailLinkChooser     = '{0}';
            window.chooserUrls.ExternalLinkChooser  = '{1}';
            // Override wagtailadmin default.
            registerHalloPlugin('hallowagtaillink');
        </script>
        """,
        reverse('wagtailadmin_choose_page_email_link'),
        reverse('wagtailadmin_choose_page_external_link')
    )

@hooks.register('register_permissions')
def register_permissions():
    content_type  = ContentType.objects.get(
        app_label   = 'wagtaillinks',
        model       = 'link'
    )

    return Permission.objects.filter(content_type=content_type)

@hooks.register('register_rich_text_link_handler')
def register_link_handler():
    #noinspection PyRedundantParentheses
    return ('link', LinkHandler)

class LinksSummaryItem(SummaryItem):
    order       = 400
    template    = 'wagtaillinks/homepage/site_summary_links.html'

    def get_context(self):
        return {
            'total_links': Link.objects.count(),
        }

@hooks.register('construct_homepage_summary_items')
def add_links_summary_item(request, items):
    items.append(LinksSummaryItem(request))