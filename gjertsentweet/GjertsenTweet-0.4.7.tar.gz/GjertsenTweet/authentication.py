from twitter import read_token_file, OAuth, oauth_dance
import os

from consumer import CONSUMER_KEY, CONSUMER_SECRET


def authenicate():
    twitter_credentials = os.path.expanduser('~/.GjertsenTweet')
    if not os.path.exists(twitter_credentials):
        oauth_dance('GjertsenTweet', CONSUMER_KEY, CONSUMER_SECRET, twitter_credentials)
    
    token, token_secret = read_token_file(twitter_credentials)

    return OAuth(token, 
                 token_secret, 
                 CONSUMER_KEY, 
                 CONSUMER_SECRET)

