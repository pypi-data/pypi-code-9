from __future__ import unicode_literals

from django.utils.html import linebreaks

from rest_framework import serializers
from textplusstuff.serializers import ExtraContextSerializerMixIn

from .models import Hashtag, Tweet, TwitterUser
from .utils import urlize_tweet


class HashtagSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Hashtag
        fields = (
            'hashtag',
            'link'
        )

    def get_link(self, obj):
        return "https://twitter.com/search?q=%23{}&src=typd".format(
            obj.hashtag
        )


class TwitterUserSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = TwitterUser
        fields = (
            'username',
            'profile_url',
            'profile_image_url'
        )

    def get_profile_url(self, obj):
        return "https://twitter.com/{}".format(
            obj.username
        )


class TweetSerializer(ExtraContextSerializerMixIn,
                      serializers.ModelSerializer):
    hashtags = HashtagSerializer(many=True)
    user = TwitterUserSerializer(many=False)
    text = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = (
            'user',
            'text',
            'hashtags',
        )

    def get_text(self, obj):
        linked_tweet = urlize_tweet(obj.text)
        return {
            'raw': obj.text,
            'urlized': linked_tweet,
            'as_html': linebreaks(linked_tweet)
        }
