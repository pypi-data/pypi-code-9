# -*- coding: utf-8 -*-

from future.utils import python_2_unicode_compatible

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fluent_contents.models.db import ContentItem


@python_2_unicode_compatible
class TwitterRecentEntriesItem(ContentItem):
    """
    Content item to display recent entries of a twitter user.

    """
    title = models.CharField(_("title"), max_length=200, blank=True,
        help_text=_("You may use Twitter markup here, such as a #hashtag or @username."))

    twitter_user = models.CharField(_("@username"), max_length=75,
        help_text=_("Display Tweets from a Twitter user specified by @username"),
    )
    amount = models.PositiveSmallIntegerField(_("number of results"), default=5)

    widget_id = models.CharField(_("widget id"), max_length=75,
        help_text=_("See <a href='https://twitter.com/settings/widgets' target='_blank'>"
                    "https://twitter.com/settings/widgets</a> on how to obtain one."),
    )

    footer_text = models.CharField(_("footer text"), max_length=200, blank=True,
        help_text=_("You may use Twitter markup here, such as a #hashtag or @username."))
    include_replies = models.BooleanField(_("include replies?"), default=False)

    def __str__(self):
        return self.title or self.twitter_user

    class Meta:
        verbose_name = _("Recent twitter entries")
        verbose_name_plural = _("Recent twitter entries")


@python_2_unicode_compatible
class TwitterSearchItem(ContentItem):
    """
    Content item to display recent entries of a twitter user.

    """
    title = models.CharField(_("title"), max_length=200, blank=True,
        help_text=_("You may use Twitter markup here, such as a #hashtag or @username."))

    query = models.CharField(_("search for"), max_length=200, default='',
        help_text=_("<a href='https://dev.twitter.com/web/embedded-timelines/search' target='_blank'>"
                    "Twitter search syntax</a> is allowed."),
    )
    amount = models.PositiveSmallIntegerField(_("number of results"), default=5)

    widget_id = models.CharField(_("widget id"), max_length=75,
        help_text=_("See <a href='https://twitter.com/settings/widgets' target='_blank'>"
                    "https://twitter.com/settings/widgets</a> on how to obtain one."),
    )

    footer_text = models.CharField(_("footer text"), max_length=200, blank=True,
        help_text=_("You may use Twitter markup here, such as a #hashtag or @username."))
    include_replies = models.BooleanField(_("include replies?"), default=False)

    def __str__(self):
        return self.title or self.query

    class Meta:
        verbose_name = _("Twitter search timeline")
        verbose_name_plural = _("Twitter search timeline")
