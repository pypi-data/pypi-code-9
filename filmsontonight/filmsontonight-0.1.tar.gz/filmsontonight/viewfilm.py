# -*- coding: utf-8 -*-
"""Uses urllib2 and BeautifulSoup to scrape www.viewfilm.net for film titles

get_titles() -- returns titles
"""

import urllib2

from BeautifulSoup import BeautifulSoup

VIEWFILM_URL = 'http://www.viewfilm.net/'


def get_titles(date='tonight'):
    """ Returns list of titles from page. Films titles are formatted in h3 tags.

    Defaults to tonight to preserve core 'filmsontonight' functionality.
    Date url format is www.viewfilm.net/date/YYYYMMDD
    """
    soup = BeautifulSoup(urllib2.urlopen(VIEWFILM_URL + date).read())
    titles = list(incident.text for incident in soup('h3'))
    return titles
