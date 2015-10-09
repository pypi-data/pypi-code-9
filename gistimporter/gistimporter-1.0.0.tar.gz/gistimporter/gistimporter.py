'''
Adds a hook to `sys.path_hooks` to handle Gists as locations for modules.
'''

import re
import sys
import encodings.idna

from contextlib import suppress
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from importlib.abc import PathEntryFinder, SourceLoader
from importlib.machinery import ModuleSpec

class gistimporter(PathEntryFinder, SourceLoader):
    '''The hook for handling Gist URLs'''

    BASE_PATH = 'https://gist.github.com/'

    GIST_REGEXP = '[^/]+/[a-f0-9]+$'

    def __init__(self, location):
        if not self.isgist(location):
            raise ImportError()
        
        self._location = location

    def find_spec(self, fullname, target=None):
        spec = None
        url = '{}/raw/{module}.py'.format(self._location, module=fullname)
        openurl = lambda: urlopen(Request(url, method='HEAD'))
        with suppress(HTTPError), openurl() as response:
            spec = ModuleSpec(fullname, self, origin=url)

        self._spec = spec
        return spec

    def get_data(self, path):
        try:
            with urlopen(self._spec.origin) as response:
                return response.read()

        except HTTPError:
            raise ImportError()

    def get_filename(self, fullname):
        return self._spec.origin

    @staticmethod
    def isgist(location):
        BASE_PATH = gistimporter.BASE_PATH
        GIST_REGEXP = gistimporter.GIST_REGEXP
        return location.startswith(BASE_PATH) and \
               re.match(GIST_REGEXP, location[len(BASE_PATH):])


def addgist(url):
    '''
    Add a new Gist location to the `sys.path`. The Gist is added in first
    place. Instead of the complete URL, you can provide just the user and
    gist hash. I.e:

        gist.addgist('https://gist.github.com/lodr/528fca98f42c5236ce1d')
        gits.addgist('lodr/528fca98f42c5236ce1d')


    '''
    sys.path.insert(0, _normalize(url))
    
def _normalize(url):
    if not url.startswith('http'):
        pathstart = 1 if url[0] == '/' else 0
        url = gistimporter.BASE_PATH + url[pathstart:]

    if not gistimporter.isgist(url):
        raise TypeError('{} is not a Gist URL'.format(url))

    return url
    

sys.path_hooks.append(gistimporter)    
