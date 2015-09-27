#!/usr/bin/env python

from argparse import ArgumentParser
from .utils import authorize, get_credentials, get_twitter
from . import ENVIRON_LOCAL, ENVIRON_STAGING, ENVIRON_PRODUCTION
from twython import TwythonError, TwythonRateLimitError, TwythonAuthError
from twython import TwythonStreamer
from .reciver import MyStreamer, reciver
from asyncio import coroutine
from butter.asyncio.eventfd import Eventfd_async as Eventfd
from collections import deque
import asyncio
import logging
import urllib3
import sys, os

RATE_LIMIT_WARN_DELAY = 900 # 15 minutes, twitters 'granularity' for api requests
UNKNOWN_ERROR_DELAY = 60

log = logging.getLogger('epic-tweet.daemon')

@coroutine
def pipe_reader(pipe, eventfd):
    log.info("Pipe reader starting up")
    while True:
        log.info("Waiting on events")
        num_events = yield from eventfd.wait()
        log.info('Message(s) recived: {}'.format(num_events))
        for i in range(num_events):
            data = pipe.popleft()
            log.info("yay message")

def main(argv=sys.argv[1:]):
    args = ArgumentParser()
    args.add_argument('-e', '--environ', choices=[ENVIRON_LOCAL, ENVIRON_STAGING, ENVIRON_PRODUCTION], default=ENVIRON_LOCAL,
        help="The enviroment the reciver is running on (disables and enables features automatically, default: %(default)s)")
    args.add_argument('-v', '--verbose', action='count', default=3,
        help="Increase the verbosity of logging")
    
    options = args.parse_args(argv)
    
    options.verbose = min(options.verbose, 4)
    log_level = {0:logging.CRITICAL,
                 1:logging.ERROR,
                 2:logging.WARN,
                 3:logging.INFO,
                 4:logging.DEBUG,
                }.get(options.verbose)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)-20s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)

    root_log = logging.getLogger("epic-tweet")
    root_log.addHandler(handler)
    root_log.setLevel(log_level)

    try:
        auth = get_credentials()
    except KeyError:
        log.critical("Could not locate authentication credentials")
        log.critical("Are the following environ vars set?: EPIC_TWEET_TWITTER_APP_KEY, EPIC_TWEET_TWITTER_APP_SECRET, EPIC_TWEET_TWITTER_OAUTH_TOKEN, EPIC_TWEET_TWITTER_OAUTH_TOKEN_SECRET")
        sys.exit(1)
        
    twitter = get_twitter() # get a twitter
    
    user = twitter.verify_credentials(
        entities=False,
        skip_status=True, # we dont want a list of status updates from the user
        )
    user_id = user['id']
    user_name = user['screen_name']
    
    log.info("Connected to user stream for @{} ({})".format(user_name, user_id))
    
    stream = MyStreamer(*auth)
    
    loop = asyncio.get_event_loop()

    eventfd = Eventfd()
    pipe = deque()
    
    p_reader = loop.create_task(pipe_reader(pipe, eventfd))

    reciver_future = loop.run_in_executor(None, reciver, twitter, stream, pipe, eventfd)

    loop.run_until_complete(reciver_future)

if __name__ == "__main__":
    sys.exit(main())
