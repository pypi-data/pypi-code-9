''' Utilities for web mining and HTML processing. '''
from bs4 import BeautifulSoup


def find_hrefs(content):
    ''' Finds href links in a HTML string.

    :param: content: A HTML string.

    :returns: A list of href links found by BeautifulSoup.
    '''
    soup = BeautifulSoup(content)

    return [a.get('href', '') for a in soup.findAll('a')]
