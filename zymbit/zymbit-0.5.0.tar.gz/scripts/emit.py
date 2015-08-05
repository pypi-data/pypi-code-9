#!/usr/bin/env python

import argparse
import datetime
import logging
import sys

from zymbit.client import Client


def timestamp():
    return datetime.datetime.utcnow().isoformat('T')


def main(action, channel, value):
    client = Client()
    client.send(action, {'key': channel, 'value': value})


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    parser = argparse.ArgumentParser()

    parser.add_argument('--action', default='data')
    parser.add_argument('channel')
    parser.add_argument('value')

    args = parser.parse_args()

    main(args.action, args.channel, args.value)
