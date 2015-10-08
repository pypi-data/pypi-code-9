#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Send Messages and files to slack from the command line.
"""

import anyconfig
from slacker import Slacker
from slacker.utils import get_item_id_by_name
import argparse
import sys
import os
import warnings
warnings.filterwarnings('ignore', message=".*InsecurePlatformWarning.*")

def post_message(token, channel, message, name, as_user, icon_emoji=None, icon_url=None):
        """ Post a message to slack """
        print("Sending Message to: {}".format(channel))
        s = Slacker(token)
        s.chat.post_message(channel, message, username=name, as_user=as_user, icon_emoji=icon_emoji, icon_url=icon_url)

def get_channel_id(token, channel_name):
        """ Get the ID of a channel"""
        s = Slacker(token)
        channels = s.channels.list().body['channels']
        return get_item_id_by_name(channels, channel_name)


def upload_file(token, channel, file_name):
        """ upload file to a channel """
        s = Slacker(token)
        channel_id = get_channel_id(token, channel)
        s.files.upload(file_name, channels=channel_id)

def merge_dicts(conf, opts):
        """ Given two dicts, merge them into a new dict as a shallow copy """
        z = conf.copy()
        z.update(opts)
        return z

def parse_args():
        """ Parse command line arguments """
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--channel", dest='channel', help="Channel to send message to")
        parser.add_argument("-u", "--user", dest='user', help="User to send message to")
        parser.add_argument("-n", "--name", dest='name', help="Slack sender name")
        parser.add_argument("-t", "--token", dest='api_token', help="Slack API token")
        parser.add_argument("-f", "--file", dest='file', help="File to upload")
        parser.add_argument("-a", "--as-user", dest='as_user', action="store_true", help="Send as the token owner")
        parser.add_argument("-i", "--icon-emoji", help="Sender emoji icon")
        parser.add_argument("--icon-url", help="Sender icon image from URL")

        args = vars(parser.parse_args())

        # Strip out args that are unset (None)
        args = { k: args[k] for k in args if args[k] != None}

        return args

def main():
        """Load the config, parse the options and do the stuff."""
        config_files=[ "/usr/local/etc/slack.yml" ]
        user_conf = os.path.join(os.path.expanduser('~'), '.slack.yml')
        if os.path.exists(user_conf) and os.path.isfile(user_conf):
                config_files.append(user_conf)
        conf = anyconfig.load( config_files )

        if 'slack' in conf:
                conf = conf['slack']
        args = parse_args()
        conf = merge_dicts(conf, args)

        message = sys.stdin.read()

        if conf.get('file', None):
                if all (k in conf for k in ('api_token', 'channel')):
                        upload_file(conf['api_token'], conf['channel'], conf['file'])

        else:
                if all (k in conf for k in ('api_token', 'channel')):
                        post_message(conf['api_token'], '#' + conf['channel'], message, conf['name'], conf['as_user'], icon_emoji=conf.get('icon_emoji', None), icon_url=conf.get('icon_url', None))

if __name__ == '__main__':
        main()
