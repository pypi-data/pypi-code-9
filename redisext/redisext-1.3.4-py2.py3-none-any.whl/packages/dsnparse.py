from __future__ import absolute_import

import sys
import re

if sys.version_info[0] == 2:
    import urlparse
elif sys.version_info[0] == 3:
    import urllib.parse as urlparse
else:
    raise RuntimeError


def parse(dsn, **defaults):
    assert re.match('^\S+://\S+', dsn), '{} is invalid, only full dsn urls (scheme://host...) allowed'.format(dsn)

    first_colon = dsn.find(':')
    scheme = dsn[0:first_colon]
    dsn_url = dsn[first_colon+1:]
    url = urlparse.urlparse(dsn_url)

    options = {}
    if url.query:
        for k, kv in urlparse.parse_qs(url.query, True, True).items():
            if len(kv) > 1:
                options[k] = kv
            else:
                options[k] = kv[0]

    r = ParseResult(
        scheme=scheme,
        hostname=url.hostname,
        path=url.path,
        params=url.params,
        query=options,
        fragment=url.fragment,
        username=url.username,
        password=url.password,
        port=url.port,
        query_str=url.query,
    )
    for k, v in defaults.items():
        r.setdefault(k, v)

    return r


class ParseResult(object):
    '''
    Hold results of a parsed dsn.

    This is very similar to urlparse.ParseResult tuple:
    http://docs.python.org/2/library/urlparse.html#results-of-urlparse-and-urlsplit

    it exposes the following attributes --
        scheme
        schemes -- if your scheme has +'s in it, then this will contain a list of schemes split by +
        path
        paths -- the path segment split by /, so '/foo/bar' would be ['foo', 'bar']
        host -- same as hostname (I just like host better)
        hostname
        hostloc -- host:port
        username
        password
        netloc
        query -- a dict of the query string
        query_str -- the raw query string
        port
        fragment
    '''
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __iter__(self):
        mapping = ['scheme', 'netloc', 'path', 'params', 'query', 'fragment']
        for k in mapping:
            yield getattr(self, k, '')

    def __getitem__(self, index):
        index = int(index)
        mapping = {
            0: 'scheme',
            1: 'netloc',
            2: 'path',
            3: 'params',
            4: 'query',
            5: 'fragment',
        }

        return getattr(self, mapping[index], '')

    @property
    def schemes(self):
        ''' Scheme, splited by `+` signs '''
        return self.scheme.split('+')

    @property
    def netloc(self):
        ''' Returns {username}:{password}@{hostname}:{port} '''
        s = ''
        prefix = ''
        if self.username:
            s += self.username
            prefix = '@'

        if self.password:
            s += ':{}'.format(self.password)
            prefix = '@'

        s += '{}{}'.format(prefix, self.hostloc)
        return s

    @property
    def paths(self):
        ''' Path attribute split by / '''
        return [_f for _f in self.path.split('/') if _f]

    @property
    def host(self):
        return self.hostname

    @property
    def hostloc(self):
        ''' Returns {host}:{port} '''
        hostloc = self.hostname
        if self.port:
            hostloc = '{}:{}'.format(hostloc, self.port)
        return hostloc

    def setdefault(self, key, val):
        if not getattr(self, key, None):
            setattr(self, key, val)

    def geturl(self):
        ''' Returns the dsn back into url form '''
        return urlparse.urlunparse((
            self.scheme,
            self.netloc,
            self.path,
            self.params,
            self.query_str,
            self.fragment,
        ))
