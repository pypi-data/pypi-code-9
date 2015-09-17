import re

from django.utils.html import urlize
from django.utils.safestring import mark_safe


def transform_tokenized_text_to_links(
    text,
    leading_character='#',
    link_class='hashtag',
    url_pattern='https://twitter.com/search?q=%23{}&src=typd'
):
    """
    Transforms any hashtags found in `text` with links as specified by
    `search_url_pattern`
    """
    reg_ex = r'(?<=^|(?<=[^a-zA-Z0-9-\\.])){token}([A-Za-z]+[A-Za-z0-9]+)'\
        .format(token=leading_character)
    reg_ex_compiled = re.compile(reg_ex)
    text = reg_ex_compiled.sub(
        lambda m: (
            '<a href="{url}" class="{link_class}" '
            'target="_blank">{item}</a>'
        ).format(
            url=url_pattern.format(m.group(1)),
            link_class=link_class,
            item=m.group(0),
        ),
        text
    )
    return text


def urlize_tweet(tweet):
    """
    Converts all 'linkable' elements in a Tweet: hashtags, usernames and links.
    """
    # Find any in-tweet links and convert them to HTML links
    tweet = urlize(tweet)
    # Link-up hashtags
    tweet = transform_tokenized_text_to_links(
        tweet,
        leading_character='#',
        link_class='hashtag',
        url_pattern='https://twitter.com/search?q=%23{}&src=typd'
    )
    # Link-up usernames
    tweet = transform_tokenized_text_to_links(
        tweet,
        leading_character='@',
        link_class='twitter-user',
        url_pattern='https://twitter.com/{}'
    )
    return mark_safe(tweet)
