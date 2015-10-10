# encoding: utf-8
"""
Processing tools for main content.
"""
from urllib.parse import urlunsplit, urlparse
from collections import namedtuple

from bs4 import BeautifulSoup


# Compatible with tuples form urllib.parse
URL = namedtuple('URL', 'scheme netloc path query fragment')
URL.__new__.__defaults__ = ('http', '', '', '', '', '')


def clean_discourse_html(html, base_url):
    base_url_parts = urlparse(base_url)
    soup = BeautifulSoup(html, 'html.parser')

    for link_tag in soup.find_all('a'):
        link_tag['href'] = make_absolute_link(link_tag['href'], base_url_parts)

    for link_tag in soup.find_all('img'):
        link_tag['src'] = make_absolute_link(link_tag['src'], base_url_parts)

    return soup.prettify()


def make_absolute_link(discourse_link, base_url_parts):
    """Make any link from Discourse into an Absolute URL.

    Discourse provides link with a '//' prefix (e.g.
    //community.lsst.org/path) or relative, e.g. (/users/jsick).
    """
    url_parts = urlparse(discourse_link, scheme='http')

    # reconstruct URL
    if len(url_parts.netloc) == 0:
        # relative (local) url; add the scheme and netloc
        return urlunsplit(URL(scheme=url_parts.scheme,
                              netloc=base_url_parts.netloc,
                              path=url_parts.path))
    else:
        # treat as a global URL
        # this roundtrip process ensures the scheme is present
        return urlunsplit(URL(scheme=url_parts.scheme,
                              netloc=url_parts.netloc,
                              path=url_parts.path))
