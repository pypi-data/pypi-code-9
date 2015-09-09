# -*- coding: utf-8 -*-
# Copyright © 2015 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Main class
'''Main class'''

import configparser
import os.path
import sys
import tweepy

from retweet.waitamoment import WaitAMoment
from retweet.cliparse import CliParse
from retweet.confparse import ConfParse


class Main(object):
    '''Main class'''
    def __init__(self):
        '''Constructor of the Main class'''
        # parse the command line
        rtargs = CliParse()
        pathtoconf = rtargs.configfile
        # read the configuration file
        cfgparse = ConfParse(pathtoconf)
        self.cfgvalues = cfgparse.confvalues

        # activate the twitter api
        self.auth = tweepy.OAuthHandler(self.cfgvalues['consumer_key'],
                                        self.cfgvalues['consumer_secret'])
        self.auth.secure = True
        self.auth.set_access_token(self.cfgvalues['access_token'],
                                    self.cfgvalues['access_token_secret'])
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.main()

    def main(self):
        '''Main of the Main class'''
        # get the 20 last tweets
        lasttweets = self.api.user_timeline(self.cfgvalues['user_to_retweet'])

        # check if retweet already ran
        if os.path.exists(self.cfgvalues['lasttweetidfile']) and os.path.isfile(self.cfgvalues['lasttweetidfile']):
            # a file with the last sent tweet id exists, using it
            with open(self.cfgvalues['lasttweetidfile']) as desc:
                lasttweetid = int(desc.read())
            print("last sent tweet:{}".format(lasttweetid))
        else:
            # no previously sent tweet, get the first one (last of the list)
            lasttweetid = lasttweets[-1].id
        # extract the last 20 tweet ids
        lasttweetids = [tweet.id for tweet in lasttweets]
        lasttweetids.reverse()
        print("last tweets:{}".format(' '.join([str(j) for j in lasttweetids])))
        if lasttweetid in lasttweetids:
            tweetstosend = lasttweetids[lasttweetids.index(lasttweetid):]
            tweetstosend.remove(lasttweetid)
            print("tweets to send:{}".format(' '.join([str(j) for j in tweetstosend])))
            for i in tweetstosend:
                try:
                    # test if it was retweeted enough to be retweeted by me
                    if len(self.api.retweets(i)) >= self.cfgvalues['retweets']:
                        self.api.retweet(i)
                        print("tweet {} sent!".format(i))
                except (tweepy.error.TweepError) as err:
                    print("{}".format(err))
                WaitAMoment(self.cfgvalues['waitminsecs'], self.cfgvalues['waitmaxsecs'])
            # if we really sent tweets, store the last one
            if len(tweetstosend) != 0:
                with open(self.cfgvalues['lasttweetidfile'], 'w') as desc:
                    desc.write(str(tweetstosend[-1]))
