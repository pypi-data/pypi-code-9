
import urllib.parse
from bl.dict import Dict

class URL(Dict):
    """Sample usage:
    >>> u = URL('http://blackearth.us:8888/this/is;really?not=something#important')
    >>> u.scheme, u.host, u.path, u.params, u.qargs, u.fragment
    ('http', 'blackearth.us:8888', '/this/is', 'really', {'not': 'something'}, 'important')
    >>> str(u)
    'http://blackearth.us:8888/this/is;really?not=something#important'
    >>> u
    URL('http://blackearth.us:8888/this/is;really?not=something#important')
    >>> u.qstring()
    'not=something'
    >>> u.drop_qarg('not')
    URL('http://blackearth.us:8888/this/is;really#important')
    >>> u                                                 # no change to u 
    URL('http://blackearth.us:8888/this/is;really?not=something#important')
"""

    def __init__(self, url='', scheme=None, host=None, path=None, params=None, 
                fragment=None, query=None, qargs={}):
        """create a URL object from the given url string."""

        # 1. parse the url string with urlparse
        if type(url) == URL:
            pr = urllib.parse.urlparse(str(url))
        else:
            pr = urllib.parse.urlparse(url)

        # 2. deal with parameters
        self.scheme     = scheme or pr.scheme
        self.host       = host or pr.netloc
        self.path       = urllib.parse.unquote(path or pr.path)
        self.params     = params or pr.params
        self.fragment   = fragment or pr.fragment

        # 3. deal with query arguments
        d = Dict(**urllib.parse.parse_qs(query or pr.query))
        for k in d:
            d[k] = d[k][-1]     # only keep the last instance of an argument
            if d[k] in [None, '']: _=d.pop('k')
        self.qargs = d
        for k in qargs.keys():
            if qargs[k] in ['', None]: 
                if k in self.qargs.keys():
                    _=self.qargs.pop(k)
            else:
                self.qargs[k] = qargs[k]

    def qstring(self):
        return urllib.parse.urlencode(self.qargs)

    def no_qargs(self):
        u = URL(**self)
        u.qargs = {}
        return u

    def drop_qarg(self, key):
        u = URL(self)
        for k in u.qargs.keys():
            if k == key:
                del(u.qargs[k])
        return u

    def __str__(self):
        pr = (self.scheme, self.host, self.path,
            self.params, self.qstring(), self.fragment)
        return urllib.parse.urlunparse(pr)

    def quoted(self):
        pr = (self.scheme, self.host, urllib.parse.quote(self.path),
            self.params, self.qstring(), self.fragment)
        return urllib.parse.urlunparse(pr)        

    def __repr__(self):
        return """URL('%s')""" % str(self)


if __name__=='__main__':
    import doctest
    doctest.testmod()
