from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

import twitter

from .fields import TweetIDField

TWITTER_API_CONFIG = getattr(settings, 'STACKS_TWITTER_API_KEYS', {})

if (
    'consumer_key' not in TWITTER_API_CONFIG
) or (
    'consumer_secret' not in TWITTER_API_CONFIG
) or (
    'access_token_key' not in TWITTER_API_CONFIG
) or (
    'access_token_secret' not in TWITTER_API_CONFIG
):
    raise ImproperlyConfigured(
        "The STACKS_TWITTER_API_KEYS setting is either unset or missing "
        "one of the required values: 'consumer_key', 'consumer_secret', "
        "'access_token_key' or 'access_token_secret'."
    )

twitter_api = twitter.Api(
    consumer_key=TWITTER_API_CONFIG['consumer_key'],
    consumer_secret=TWITTER_API_CONFIG['consumer_secret'],
    access_token_key=TWITTER_API_CONFIG['access_token_key'],
    access_token_secret=TWITTER_API_CONFIG['access_token_secret']
)


class TwitterUser(models.Model):
    """Represents a Twitter user."""

    username = models.CharField(
        _('Twitter Username'),
        max_length=15,
        unique=True
    )
    verbose_name = models.CharField(
        _('Verbose Name'),
        max_length=140,
        blank=True
    )
    profile_image_url = models.URLField(
        _('Profile Image URL'),
        blank=True,
        max_length=255
    )

    class Meta:
        verbose_name = 'Twitter User'
        verbose_name_plural = 'Twitter Users'

    def __unicode__(self):
        return "@%s" % self.username

    def save(self):
        process_via_twitter_api = True
        # Check to see if this user should be processed by querying the API
        # Step 1: If this instance has a primary key (pk) it has already
        # been created so...
        if self.pk:
            # ...pull the existing record from the database
            orig = self.__class__.objects.get(pk=self.pk)
            # If the existing cove_id is the same as this one it means
            # that it hasn't changed so...
            if str(orig.username) == str(self.username):
                # we don't need to re-query the API
                process_via_twitter_api = False

        if process_via_twitter_api:
            try:
                user = twitter_api.GetUser(screen_name=self.username)
            except twitter.TwitterError:
                raise ValidationError(
                    "The `Username` you entered did not return a current "
                    "user of Twitter."
                )
            else:
                self.verbose_name = user.name
                self.profile_image_url = user.profile_image_url

        super(TwitterUser, self).save()


class Hashtag(models.Model):
    """Represents a Twitter Hashtag."""

    hashtag = models.CharField(
        _('Hashtag'),
        unique=True,
        db_index=True,
        max_length=140
    )

    class Meta:
        verbose_name = _('Hashtag')
        verbose_name_plural = _('Hashtags')

    def __unicode__(self):
        return self.hashtag


class Tweet(models.Model):
    """Represents a Tweet."""

    tweet_id = TweetIDField(
        _('Tweet Link / Tweet ID'),
        help_text="Enter a link to a tweet or a Tweet ID in this field."
    )
    user = models.ForeignKey(
        TwitterUser,
        verbose_name=_('User'),
        blank=True
    )
    text = models.TextField(
        _('Tweet Text'),
        max_length=200,
        blank=True,
    )
    hashtags = models.ManyToManyField(
        'Hashtag',
        blank=True
    )
    tweet_link = models.URLField(
        _('Link To Tweet'),
        blank=True,
        max_length=255
    )

    class Meta:
        verbose_name = _('Tweet')
        verbose_name_plural = _('Tweets')

    def __unicode__(self):
        return "@%s: %s" % (self.user.username, self.text)

    def save(self):
        process_via_twitter_api = True
        # Check to see if the tweet should be processed by querying the API
        # Step 1: If this instance has a primary key (pk) it has already
        # been created so...
        if self.pk:
            # ...pull the existing record from the database
            orig = self.__class__.objects.get(pk=self.pk)
            # If the existing cove_id is the same as this one it means
            # that it hasn't changed so...
            if str(orig.tweet_id) == str(self.tweet_id):
                # we don't need to re-query the API
                process_via_twitter_api = False

        if process_via_twitter_api:
            tweet_id = int(self.tweet_id)
            try:
                status = twitter_api.GetStatus(id=tweet_id)
            except twitter.TwitterError:
                raise ValidationError(
                    "The `Tweet ID` you entered did not return a Tweet "
                    "from the Twitter API."
                )
            else:
                try:
                    user = TwitterUser.objects.get(
                        username=status.user.screen_name
                    )
                except TwitterUser.DoesNotExist:
                    user = TwitterUser(
                        username=status.user.screen_name
                    )
                    user.save()
                self.text = status.text
                self.user = user
                self.tweet_link = "https://twitter.com/%s/status/%d" % (
                    user.username,
                    self.tweet_id
                )
                super(Tweet, self).save()
                for hashtag in status.hashtags:
                    ht, created = Hashtag.objects.get_or_create(
                        hashtag=hashtag.text
                    )
                    self.hashtags.add(ht.pk)
        else:
            super(Tweet, self).save()
