# encoding: utf-8
"""
Forward new topics in selected Discourse categories to select email addresses
using Mandrill.

This script is intended to be run as a repeated task that pulls new topics
and forward the HTML content of the topic's first post to email recipents
through Mandrill. When topics are forwarded, they are also cached.

Specific Discourse categories can be monitoried, and each category can have
topics forwarded to one or more email recipients. The map file (see below)
figures the email recipeints for selected categories.

Map file
--------

The ``map_file`` argument should be set to the path of a JSON file that
category IDs to email recipients. The format is::

    {
        "<id>": [{"email": "<email address>",
                  "name": "<recipient name>",
                  "type": "to"}],
    }

See ``config.json`` in the ``community_mailbot`` project repository for a
working example.

The ``discourse_categories`` script, also in the project, lets you discover
the category IDs relative to their human-readable names.
"""

import os
import json
from argparse import ArgumentParser, RawDescriptionHelpFormatter

import requests
import mandrill

from community_mailbot.discourse import (CategoryFeed, TopicFeed, TopicCache,
                                         SiteFeed)
from community_mailbot.contentpipe import clean_discourse_html


def main():
    args = parse_args()

    with open(args.map_file, 'r') as f:
        mapping = json.load(f)

    forward_new_topics(mapping, args.cache,
                       args.url,  args.key, args.user,
                       args.mandrill, args.cache_only)


def parse_args():
    cache_default = os.getenv(
        'COMMUNITY_MAILBOT_CACHE',
        os.path.expandvars('$HOME/.community_mailbot_cache'))
    default_url = 'http://community.lsst.org'
    default_mandrill_key = os.getenv('MANDRILL_KEY', None)
    default_discourse_key = os.getenv('DISCOURSE_KEY', None)
    default_discourse_user = os.getenv('DISCOURSE_USER', None)

    parser = ArgumentParser(
        prog='forward_discourse',
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument(
        'map_file',
        help='Path to JSON file mapping categories to E-mail addresses')
    parser.add_argument(
        '--cache',
        help='Path to the topic cache file (or $COMMUNITY_MAILBOT_CACHE)',
        default=cache_default)
    parser.add_argument(
        '--key',
        default=default_discourse_key,
        help='Discourse API key (or $DISCOURSE_KEY)')
    parser.add_argument(
        '--user',
        default=default_discourse_user,
        help='Discourse API user (or $DISCOURSE_USER)')
    parser.add_argument(
        '--url',
        default=default_url,
        help='Base URL of the discourse forum')
    parser.add_argument(
        '--mandrill',
        default=default_mandrill_key,
        help='MANDRILL API key (or $MANDRILL_KEY)')
    parser.add_argument(
        '--cache-only',
        default=False,
        action='store_true',
        help='Do not send emails, process and cache topics only')
    return parser.parse_args()


def forward_new_topics(mapping, cache_path,
                       base_url, discourse_key, discourse_user,
                       mandrill_key, cache_only):
    """Coordinating function.

    Each category is processed and the cache is persisted at the end.
    """
    cache = TopicCache(cache_path)
    site_feed = SiteFeed(base_url, key=discourse_key, user=discourse_user)
    category_names = site_feed.category_names
    category_paths = site_feed.category_paths

    for category_id, recipients in mapping.items():
        cat_feed = CategoryFeed(category_paths[int(category_id)], base_url,
                                key=discourse_key, user=discourse_user)
        for topic in cat_feed.new_topics(cache):
            forward_topic(topic.slug, topic.iid, category_id,
                          recipients, cache,
                          base_url, discourse_key, discourse_user,
                          mandrill_key, cache_only,
                          category_names[int(category_id)])
            cache.save()


def forward_topic(topic_slug, topic_id, category_id, recipients, cache,
                  base_url, discourse_key, discourse_user, mandrill_key,
                  cache_only, category_name):
    """Forward a topic post to the destination email addresses.

    The topic is cached once it is successfuly posted.
    """
    print(topic_slug)
    try:
        topic = TopicFeed(topic_slug, topic_id, base_url,
                          key=discourse_key, user=discourse_user)
    except requests.exceptions.HTTPError:
        print('Bad Permissions {0} (skipping)'.format(topic_slug))
        return

    if int(topic.category_id) != int(category_id):
        # ensure topics from sub-categories aren't included
        print('skipping {0}, {1} is not {2}'.format(topic_slug,
              topic.category_id,
              category_id))
        return

    # FIXME testing
    print('Sending', topic.title, 'to', [r['email'] for r in recipients])

    if not cache_only:
        # docs:
        # https://mandrillapp.com/api/docs/messages.python.html#method-send
        # https://mandrill.zendesk.com/hc/en-us/articles/205582487-How-do-I-use-merge-tags-to-add-dynamic-content-

        # Build messsage content
        template_content = []
        global_merge = [
            {'name': 'BODY_CONTENT',
             'content': topic.first_post_content},
            {'name': 'TOPIC_URL',
             'content': topic.html_url},
            {'name': 'TOPIC_AUTHOR',
             'content': topic.first_post_author_real_name}
        ]
        subject = '[{category}] {title}'.format(category=category_name,
                                                title=topic.title)
        cleaned_html = clean_discourse_html(topic.first_post_content, base_url)
        message = {
            'from_email': 'noreply@community.lsst.org',
            'from_name': topic.first_post_author_real_name,
            'to': recipients,
            'preserve_recipients': False,  # don't expose recipients
            'auto_text': True,
            'track_opens': True,
            'track_clicks': False,
            'signing_domain': None,  # TODO
            'subaccount': 'community_mailbot',
            'subject': subject,
            'html': cleaned_html,
            'global_merge_vars': global_merge,
        }

        # Send message with Mandrill
        mandrill_client = mandrill.Mandrill(mandrill_key)
        try:
            result = mandrill_client.messages.send_template(
                template_name='community-mailbot-template-2',
                template_content=template_content,
                message=message,
                async=False)
        except mandrill.Error as e:
            print(result)
            print('A mandrill error occurred: %s - %s' % (e.__class__, e))
            raise
        print(result)

    # Cache the topic only when we know it was sent
    cache.add(topic_slug,
              category_id=topic.category_id,
              created_at=topic.datetime_iso)


if __name__ == '__main__':
    main()
