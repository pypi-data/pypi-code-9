import os
import requests
from redis import StrictRedis
from textwrap import dedent
from textblob import TextBlob

R = StrictRedis.from_url(os.environ['REDIS_URL'])
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']


class BaseReview(object):

    type = None

    SLACK_TEMPLATE = dedent('''
        New {self.type} by {self.author}:

        >>>{self.text}
    ''').strip()


    def __init__(self, review_id, text, rating=None, author=None):
        assert self.type is not None
        self.id = review_id
        self.text = text
        self._rating = rating
        self._author = author
        self.is_new = R.sadd('starpicker:seen_review_ids', self.redis_key) == 1

    @property
    def redis_key(self):
        return '{self.type}:{self.id}'.format(self=self)

    @property
    def author(self):
        return self._author

    @property
    def rating(self):
        if self._rating:
            return self._rating
        else:
            blob = TextBlob(self.text)
            if blob.detect_language() == 'en':
                return round(min(max(blob.sentiment.polarity, -0.5), 0.5) * 4 + 3)

    def send_to_slack(self):
        color_map = {1: 'danger', 2: 'warning', 3: 'warning', 5: 'good'}

        body = {
            'username': 'starpicker',
            'attachments': [
                {
                    'fallback': self.SLACK_TEMPLATE.format(self=self),
                    'pretext': self.SLACK_TEMPLATE.format(self=self).split('\n')[0],
                    'text': self.text,
                    'color': color_map.get(self.rating),
                    'title': '{self.type} #{self.id}'.format(self=self),
                    'title_link': self.url,
                    'fields': [
                        {
                            'title': 'Author',
                            'value': self.author,
                            'short': True,
                        },
                        {
                            'title': 'Rating',
                            'value': self.rating or '?',
                            'short': True,
                        },
                    ]
                }
            ]
        }

        requests.post(SLACK_WEBHOOK_URL, json=body)


class TrustpilotReview(BaseReview):

    type = 'trustpilot.com review'

    @classmethod
    def from_source(cls, tag):
        body = '\n\n'.join(
            tag.strip()
            for tag in tag.find('div', 'review-body').contents
            if isinstance(tag, str)
        )
        rating = int(tag.find('meta', itemprop='ratingValue')['content'])
        author = tag.find('div', 'user-review-name').find('span', itemprop='name').text
        return cls(tag['data-reviewmid'], body, rating, author)

    @property
    def url(self):
        return 'https://www.trustpilot.com/review/skypicker.com/{self.id}'.format(self=self)


class FacebookRatingReview(BaseReview):

    type = 'Facebook review'

    @classmethod
    def from_source(cls, rating):
        return cls(rating['open_graph_story']['id'], rating['review_text'], rating['rating'], rating['reviewer']['name'])

    @property
    def url(self):
        return 'https://www.facebook.com/{self.id}'.format(self=self)


class FacebookCommentReview(BaseReview):

    type = 'Facebook comment'

    @classmethod
    def from_source(cls, comment):
        return cls(comment['id'], comment['message'], comment['from']['name'])

    @property
    def url(self):
        return 'https://www.facebook.com/{0}'.format(self.id.split('_')[0])


class TweetReview(BaseReview):

    type = 'tweet'

    @classmethod
    def from_source(cls, tweet):
        sentiment_map = {':(': 1, '': None, ':)': 5}
        return cls(tweet['id'], tweet['text'], rating=sentiment_map[sentiment], author=tweet['user'])

    @property
    def url(self):
        return 'https://www.twitter.com/{self._author[screen_name]}/status/{self.id}'.format(self=self)

    @property
    def author(self):
        return self._author['name']
