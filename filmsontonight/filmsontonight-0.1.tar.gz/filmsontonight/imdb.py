# -*- coding: utf-8 -*-
"""Uses BeautifulSoup and urllib2 to open IMDB search page and scrape the first
link for a title.

_parse_soup(title) -- Non-public, used by get_link find first link in soup.
get_link(index) --  Calls csv_handler and returns title with link to IMDB.
"""

import urllib2

from BeautifulSoup import BeautifulSoup

import csv_handler

IMDB_URL = 'http://www.imdb.com/'
IMDB_SEARCH_URL = IMDB_URL + 'find?s=all&q='


def _parse_soup(title):
    """Uses IMDB's search functionality and returns first result link.

    Keyword arguments:
    title -- retrieved from films.csv and appended to IMDB_SEARCH_URL
    """
    # 'I'm Feeling Lucky' for IMDB.
    search = IMDB_SEARCH_URL + title.replace(' ', '+')
    soup = BeautifulSoup(urllib2.urlopen(search).read())
    result = soup.first('td', { 'class' : 'result_text' })
    if result:
        href = result.find('a').get('href')
        return IMDB_URL + href[:17] # Cut string at end of IMDB unique identifier
    else:
        return "No link found"

def get_link(index):
    """Calls csv_handler with index and returns title with link to IMDB.

    Keyword arguments:
    index -- passed to csv_handler
    """
    result = csv_handler.get_title(index)
    if result[:5] == 'Error':
        return result
    else:
        return result + ': ' + _parse_soup(result)
