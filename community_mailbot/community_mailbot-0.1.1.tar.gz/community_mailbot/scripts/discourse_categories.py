# encoding: utf-8
"""
List categories and their IDs in a Discourse forum.
"""

import os
from argparse import ArgumentParser
from community_mailbot.discourse import SiteFeed


def main():
    args = parse_args()

    site_feed = SiteFeed(args.url, user=args.user, key=args.key)
    for c_id, name in site_feed.category_names.items():
        print(c_id, name)


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        '--key',
        default=os.getenv('DISCOURSE_KEY', None),
        help='Discourse API key')
    parser.add_argument(
        '--user',
        default=os.getenv('DISCOURSE_USER', None),
        help='Discourse API user')
    parser.add_argument(
        '--url',
        default='http://community.lsst.org',
        help='Base URL of the discourse forum')
    return parser.parse_args()


if __name__ == '__main__':
    main()
