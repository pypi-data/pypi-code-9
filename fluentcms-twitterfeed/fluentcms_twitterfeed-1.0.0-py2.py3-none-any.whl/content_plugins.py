# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import ContentPlugin, plugin_pool

from .models import TwitterRecentEntriesItem, TwitterSearchItem


@plugin_pool.register
class TwitterRecentEntriesPlugin(ContentPlugin):
    """
    The plugin to display recent twitter entries of a user.
    """
    category = _('Media')
    model = TwitterRecentEntriesItem
    render_template = "fluentcms_twitterfeed/recent_entries.html"

    class FrontendMedia:
        js = ('//platform.twitter.com/widgets.js',)


@plugin_pool.register
class TwitterSearchPlugin(ContentPlugin):
    """
    The plugin to display recent twitter entries of a user.
    """
    category = _('Media')
    model = TwitterSearchItem
    render_template = "fluentcms_twitterfeed/search.html"

    class FrontendMedia:
        js = ('//platform.twitter.com/widgets.js',)
