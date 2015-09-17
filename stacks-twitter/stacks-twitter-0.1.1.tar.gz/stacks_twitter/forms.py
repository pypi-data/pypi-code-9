from django.forms import ModelForm

from .models import Tweet


class TweetCreateForm(ModelForm):

    class Meta:
        model = Tweet
        fields = (
            'tweet_id',
        )


class TweetEditForm(ModelForm):

    class Meta:
        model = Tweet
        fields = (
            'user',
            'text',
            'tweet_id',
            'hashtags',
            'tweet_link'
        )
