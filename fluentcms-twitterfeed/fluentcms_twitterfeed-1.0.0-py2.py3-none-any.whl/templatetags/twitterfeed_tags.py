# -*- coding: utf-8 -*-

from django.template import Library
from django.utils.safestring import mark_safe

from twitter_text import TwitterText

register = Library()

@register.filter
def urlize_twitter(text):
    """
    Replace #hashtag and @username references in a tweet with HTML text.
    """
    html = TwitterText(text).autolink.auto_link()
    return mark_safe(html.replace(
        'twitter.com/search?q=', 'twitter.com/search/realtime/'))
