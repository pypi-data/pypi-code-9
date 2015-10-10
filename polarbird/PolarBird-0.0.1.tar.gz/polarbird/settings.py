DATETIME_FORMAT = '%H:%M'

TWEET_FORMAT = '[{tweet[created_at]}] <{tweet[user][screen_name]}> {tweet[text]}'

RETWEET_FORMAT = (
    '[{tweet[created_at]}] <{tweet[user][screen_name]}> RT '
    '@{tweet[retweeted_status][user][screen_name]} {tweet[retweeted_status][text]}'
)

from user_settings import *  # NOQA
