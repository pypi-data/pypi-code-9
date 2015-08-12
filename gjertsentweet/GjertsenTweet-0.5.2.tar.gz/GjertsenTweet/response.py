import time
import datetime
from functools import wraps

import dict_digger


month_names = ['Jan','Feb','Mar','Apr','May','Jun', 
               'Jul','Aug','Sep','Oct','Nov','Dec']

months = {month: i+1 for i, month in enumerate(month_names)}


class Response(object):
    """A non-data descriptor to do more elegant lookups in 
       the twitter response json """
    def __init__(self, *path):
        self.path = path

    def __get__(self, instance, cls):
        try:
            return dict_digger.dig(instance.response, *self.path, fail=True)
        except KeyError, IndexError:
            return None


class TwitterResponse(object):
    """Class to hold a twitter response from the twitter response json"""
    def __init__(self, response):
        self.response = response

    username = Response('user', 'screen_name')
    full_name = Response('user','name')
    tweet_text = Response('text')
    created_at = Response('created_at')


def attribute_safe(func):
    """Decorator used by functions that try to access 
       attributes from its local variables in order to 
       abstract the try/except block away"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError:
            return None
    return wrapper


def strip_leading_zero(month):
    if month.startswith('0'):
        return int(month[1:])
    return int(month)


def adjust_time(timestamp):
    """Adjusts the time provided by twitter to the current local time"""
    # dst = daylight saving time
    if time.localtime(timestamp).tm_isdst:
        return timestamp - time.altzone
    return timestamp - time.timezone


def make_timestamp(tweet_time, time_format):
    """Creates a timestamp based on the time attached to a tweet"""
    tweet_time = tweet_time.split()
    month = months[tweet_time[1]]
    day = tweet_time[2]
    ttime = tweet_time[3]
    year = tweet_time[5]
    tweet_time = '{} {} {} {}'.format(ttime, month, day, year)
    timestamp = time.mktime(datetime.datetime.strptime(tweet_time, time_format).timetuple())
    return adjust_time(timestamp)


def format_time(tweet_time):
    """Formats the time provided by twitter so it looks nice
       and show the right time."""
    time_format = '%H:%M:%S %m %d %Y'
    timestamp = make_timestamp(tweet_time, time_format)
    tweet_time = datetime.datetime.fromtimestamp(timestamp).strftime(time_format).split()
    tweet_time[1] = month_names[strip_leading_zero(tweet_time[1])-1]
    return ' '.join(tweet_time)


def find_break_point(string, screen_width):
    """Finds the best index to split a string, in order
       to make it fit in a terminal. This is because npyscreen
       doesn't add a newline for you, instead it will continue
       writing the string outside the screen."""
    last_space = 0
    for i in range(len(string)):
        if string[i] == ' ':
            last_space = i
        if i > screen_width-7:
            return last_space+1
    return screen_width


# npyscreen doesn't resize its widgets and forms when
# the screensize is <80
def format_tweet(string, screen_width):
    """Splits a tweet into two lines if it's too long
       to fit the screen"""
    index = find_break_point(string, screen_width)
    line1 = string[0:index]
    line2 = string[index:]
    return [line1, ''] if line2 == '' else [line1, line2, '']


@attribute_safe
def parse_tweet(data, screen_width):
    """Parses the data to get the interesting data.
       Returns a list thats contains data we are interested in,
       or None if it got an keyError on any of the lookups."""
    response = TwitterResponse(data)
    
    username = '@{}'.format(response.username.encode('utf8', 'replace'))
    full_name = response.full_name.encode('utf8', 'replace')
    tweet_text = format_tweet(response.tweet_text.encode('utf8', 'replace'), screen_width)
    time = format_time(response.created_at)

    parsed_tweet = [full_name, username, time]
    for text in tweet_text:
        parsed_tweet.append(text)
    
    return parsed_tweet

