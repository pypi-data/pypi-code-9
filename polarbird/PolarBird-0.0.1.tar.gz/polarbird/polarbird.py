import os
import threading
import twitter

from polarbird import USER_DIR
from polarbird.tokens import TOKENS_FILE, CONSUMER_KEY, CONSUMER_SECRET
from polarbird.commands import CommandLine
from polarbird.printers import print_tweet, print_retweet
from polarbird.tweets import TweetDatabase

class PolarBird(object):
    """
    Main class that everything starts. Creates OAuth instance for
    authentication to Twitter.
    """

    def __init__(self):
        self._create_user_dir()
        self.auth = self._get_oauth()
        self.tweet_database = TweetDatabase()
        self.stream_thread = None
        self._create_stream_thread()
        cl = CommandLine(self)
        cl.listen()

    def _get_oauth(self):
        """
        Read token file for tokens, if exists, or get new tokens from Twitter
        and return OAuth instance.
        """
        if not os.path.exists(TOKENS_FILE):
            token, token_key = twitter.oauth_dance(
                'PolarBird', CONSUMER_KEY,
                CONSUMER_SECRET, TOKENS_FILE
            )
        else:
            token, token_key = twitter.read_token_file(TOKENS_FILE)
        auth = twitter.OAuth(
            token, token_key, CONSUMER_KEY, CONSUMER_SECRET
        )

        return auth

    def _create_user_dir(self):
        if not os.path.isdir(USER_DIR):
            os.makedirs(USER_DIR)

    def _create_stream_thread(self):
        self.stream_thread = threading.Thread(target=self._new_tweets_stream)
        self.stream_thread.daemon = True
        self.stream_thread.start()

    def _new_tweets_stream(self):
        stream = self._get_public_stream()
        tweets = stream.user()
        for tweet in tweets:
            if tweet.get('hangup'):
                print('<< Reconnecting to Twitter stream...')
                stream = self._get_public_stream()
                tweets = stream.user()
            elif tweet.get('text'):
                key = self.tweet_database.insert(tweet)
                if 'retweeted_status' in tweet:
                    print_retweet(tweet, key, notify=True)
                else:
                    print_tweet(tweet, key, notify=True)

    def _get_public_stream(self):
        stream = twitter.TwitterStream(
            auth=self.auth, domain='userstream.twitter.com'
        )

        return stream
