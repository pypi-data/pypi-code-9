# encoding: utf-8
"""
Tools for reading the JSON API from a Discourse site.
"""

import os
from urllib.parse import urlunsplit, urlparse
import json
from collections import namedtuple

import requests


# Compatible with tuples form urllib.parse
URL = namedtuple('URL', 'scheme netloc path query fragment')
URL.__new__.__defaults__ = ('http', '', '', '', '', '')

# Identification for a topic
TopicID = namedtuple('TopicID', 'iid slug')


class SiteFeed(object):
    """Access to Discourse's site.json

    Parameters
    ----------
    base_url : str
        Root URL of the Discourse forum.
    key : str, optional
        Discourse API key, needed for working with private categories.
    user : str, optional
        Discourse API username, needed for working with private categories.
    """
    def __init__(self, base_url, key=None, user=None):
        super(SiteFeed, self).__init__()
        self._base_url = base_url
        self._key = key
        self._user = user

        self._feed = self._fetch_feed()

    @property
    def url(self):
        """JSON feed URL."""
        parts = urlparse(self._base_url, scheme='http', allow_fragments=True)
        return urlunsplit(URL(scheme=parts.scheme,
                              netloc=parts.netloc,
                              path='site.json'))

    def _fetch_feed(self):
        """Get the category's JSON feed and parse it into a Python dict."""
        params = {}
        if (self._key is not None) and (self._user is not None):
            params['api_key'] = self._key
            params['api_user'] = self._user
        r = requests.get(self.url, params=params)
        print(r.url)
        r.raise_for_status()  # can raise requests.exceptions.HTTPError
        return r.json()

    @property
    def category_names(self):
        """dict mapping category ID (int) to the full category name (str)."""
        return {c['id']: c['name'] for c in self._feed['categories']}

    @property
    def category_paths(self):
        """dict mapping category ID (int) to the category's URL path."""
        paths = {}

        # first pass: get only primary categories
        for c in self._feed['categories']:
            if 'parent_category_id' not in c:
                paths[c['id']] = c['slug']

        # second pass: get subcategories
        for c in self._feed['categories']:
            if 'parent_category_id' in c:
                parent_slug = paths[c['parent_category_id']]
                paths[c['id']] = '/'.join((parent_slug, c['slug']))

        return paths


class CategoryFeed(object):
    """JSON feed from a specific category.

    Parameters
    ----------
    category_path : str
        The category's URL path.
    base_url : str
        Root URL of the Discourse forum.
    key : str, optional
        Discourse API key, needed for working with private categories.
    user : str, optional
        Discourse API username, needed for working with private categories.
    """
    def __init__(self, category_path, base_url, key=None, user=None):
        super().__init__()
        self._category_path = category_path
        self._base_url = base_url
        self._key = key
        self._user = user

        self._feed = self._fetch_feed()

    @property
    def url(self):
        """JSON feed URL."""
        parts = urlparse(self._base_url, scheme='http', allow_fragments=True)
        url = URL(scheme=parts.scheme,
                  netloc=parts.netloc,
                  path='c/{0}/l/latest.json'.format(self._category_path))
        return urlunsplit(url)

    def _fetch_feed(self):
        """Get the category's JSON feed and parse it into a Python dict."""
        params = {}
        if (self._key is not None) and (self._user is not None):
            params['api_key'] = self._key
            params['api_user'] = self._user
        r = requests.get(self.url, params=params)
        print(r.url)
        r.raise_for_status()  # can raise requests.exceptions.HTTPError
        return r.json()

    def new_topics(self, cache):
        """New topics in the feed that aren't cached.

        Parameters
        ----------
        cache : :class:`TopicCache`
            A :class:`TopicCache` instance.

        Returns
        -------
        topic_list : list
            A list of new ``TopicID`` tuples with attributes ``iid`` (``int``)
            and ``slug`` (``str``) of topics that aren't in the cache.
        """
        return [TopicID(iid=t['id'], slug=t['slug'])
                for t in self._feed['topic_list']['topics']
                if t['slug'] not in cache]


class TopicFeed(object):
    """JSON feed from a Discourse topic.

    Parameters
    ----------
    topic_slug : str
        Slug of the topic
    topic_id : int
        ID of the topic
    base_url : str
        Root URL of the Discourse forum.
    key : str, optional
        Discourse API key, needed for working with private categories.
    user : str, optional
        Discourse API username, needed for working with private categories.
    """
    def __init__(self, topic_slug, topic_id, base_url,
                 key=None, user=None):
        super().__init__()
        self._id = topic_id
        self._slug = topic_slug
        self._base_url = base_url
        self._key = key
        self._user = user

        self._feed = self._fetch_feed()

    @property
    def url(self):
        """JSON feed URL."""
        parts = urlparse(self._base_url, scheme='http', allow_fragments=True)
        url = urlunsplit(URL(scheme=parts.scheme,
                             netloc=parts.netloc,
                             path='t/{0:d}.json'.format(self._id)))
        return url

    def _fetch_feed(self):
        """Get the topic's JSON feed and parse it into a Python dict."""
        # Surprisingly requests is not adding these parameters to my URL!
        params = {}
        if (self._key is not None) and (self._user is not None):
            params['api_key'] = self._key
            params['api_user'] = self._user
        r = requests.get(self.url, params=params)
        print(r.url)
        r.raise_for_status()  # can raise requests.exceptions.HTTPError
        return r.json()

    @property
    def slug(self):
        """Slug (URL shortname) of the topic."""
        return self._slug

    @property
    def html_url(self):
        """Topic HTML URL."""
        parts = urlparse(self._base_url, scheme='http', allow_fragments=True)
        return urlunsplit(URL(scheme=parts.scheme,
                              netloc=parts.netloc,
                              path='t/{0}'.format(self._slug)))

    @property
    def datetime_iso(self):
        """ISO datetime string of first post in topic"""
        return self._feed['post_stream']['posts'][0]['created_at']

    @property
    def category_id(self):
        """The topic's category (``int`` ID)."""
        return self._feed['category_id']

    @property
    def title(self):
        """The topic's title."""
        return self._feed['title']

    @property
    def first_post_content(self):
        """Content of the topic's first post, as HTML (latest revision)."""
        return self._feed['post_stream']['posts'][0]['cooked']

    @property
    def first_post_author_real_name(self):
        """Display name of the topic's original poster."""
        return self._feed['post_stream']['posts'][0]['display_username']


class TopicCache(object):
    """Cache of topics already seen/processed.

    The cache is stored in a JSON-formatted file. The parent object is a
    ``dict``, keyed by the topic's slug. Value is a dict with fields

    - `created_at` (an ISO datetime string)
    - `category` (a string)

    .. note::

        In the future this JSON cache could be converted into an sqlite DB
        for performance.

    Parameters
    ----------
    cache_path : str
        File path to the cache file. The cache will be created if it does
        not alreay exist.
    """
    def __init__(self, cache_path):
        super(TopicCache, self).__init__()
        self._path = cache_path

        try:
            self._cache = self._load_cache()
        except IOError:
            # start a brand new cache
            self._cache = {}

    def _load_cache(self):
        with open(self._path, 'r') as f:
            cache = json.load(f)
        return cache

    def __len__(self):
        return len(self._cache)

    def __getitem__(self, key):
        return self._cache[key]

    def __contains__(self, key):
        if key in self._cache:
            return True
        else:
            return False

    def add(self, topic_slug, category_id=None, created_at=None):
        """Add a topic to the cache.

        Parameters
        ----------
        topic_slug : str
            The url-friendly shortname for the topic. Topics are keyed in the
            cache by slug.
        category_id : int
            The identifier for the category containing the topic.
        created_at : str
            The ISO datetime string for when the topic was created.
        """
        self._cache[topic_slug] = {'category_id': category_id,
                                   'created_at': created_at}

    def save(self):
        """Save the cache onto the filesystem."""
        dirname = os.path.dirname(self._path)
        if (dirname is not '') and (os.path.exists(dirname) is False):
            os.makedirs(dirname)

        with open(self._path, 'w') as f:
            json.dump(self._cache, f, indent=2)
