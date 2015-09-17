from urlparse import urlparse

from django.forms import ValidationError
from django.db import models


class TweetIDField(models.CharField):
    """
    Accepts either a link to a tweet on twitter.com or a raw Tweet ID

    If a link is entered into the field it will be parsed and converted
    into a Tweet ID
    """
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'unique': True,
            'max_length': 255
        })
        super(TweetIDField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(TweetIDField, self).clean(*args, **kwargs)
        try:
            tweet_id = int(data)
        except ValueError:
            tweet_link_parsed = urlparse(data)
            if not tweet_link_parsed.scheme or not tweet_link_parsed.netloc:
                raise ValidationError(
                    "Could not discern a Tweet ID based on the value entered "
                    "into this field. Either enter a valid Tweet ID or a link "
                    "to a tweet on twitter.com"
                )
            elif 'twitter.com' not in tweet_link_parsed.netloc:
                raise ValidationError(
                    "An invalid URL was entered. Only links to tweets on "
                    "twitter.com can be processed by this field."
                )
            else:
                try:
                    tweet_id = int(tweet_link_parsed.path.split('/')[-1])
                except ValueError:
                    raise ValidationError(
                        "An invalid URL on twitter.com was entered. Only "
                        "links to individual tweets can be processed by "
                        "this field."
                    )
        return tweet_id
