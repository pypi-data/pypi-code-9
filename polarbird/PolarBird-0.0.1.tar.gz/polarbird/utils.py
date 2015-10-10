from datetime import datetime
from pgi.repository import Notify

from polarbird.settings import DATETIME_FORMAT

DATETIME_ORIGINAL_FORMAT = '%a %b %d %H:%M:%S %z %Y'

def convert_datetime(tweet):
    """
    Converts datetime format of tweet to user defined format
    and replaces the original
    """
    dt = datetime.strptime(tweet['created_at'], DATETIME_ORIGINAL_FORMAT)
    dt = dt.astimezone()
    tweet['created_at'] = dt.strftime(DATETIME_FORMAT)

def show_notification(tweet, is_retweet=False):
    if is_retweet:
        username = '@{}'.format(tweet['retweeted_status']['user']['screen_name'])
        text = tweet['retweeted_status']['text']
    else:
        username = '@{}'.format(tweet['user']['screen_name'])
        text = tweet['text']
    Notify.init('PolarBird')
    n = Notify.Notification.new(username, text, 'dialog-information')
    n.show()
