from polarbird.settings import TWEET_FORMAT, RETWEET_FORMAT
from polarbird.colors import colors
from polarbird.utils import convert_datetime, show_notification

def print_tweet(tweet, key, notify=False):
    """
    Print regular tweet with user defined format
    """
    if notify:
        show_notification(tweet)
    convert_datetime(tweet)
    print(TWEET_FORMAT.format(tweet=tweet, key=key, colors=colors))

def print_retweet(tweet, key, notify=False):
    """
    Print retweet with user defined format
    """
    if notify:
        show_notification(tweet, is_retweet=True)
    convert_datetime(tweet)
    print(RETWEET_FORMAT.format(tweet=tweet, key=key, colors=colors))

def print_twitter_error(error):
    for error in error.response_data.get('errors', dict()):
        print(colorize(error.get('message'), colors['yellow']))

def colorize(text, color):
    colorized_text = '{color}{text}{white}'.format(
        color=color, text=text, white=colors['white']
    )

    return colorized_text
