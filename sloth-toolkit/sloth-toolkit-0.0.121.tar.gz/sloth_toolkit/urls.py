import urlparse
import requests
from bs4 import BeautifulSoup as BS

from . import verify


def is_lazyurl(obj, raise_error=False):
    return verify.is_type_of(obj, LazyUrl, raise_error)



class LazyUrl (object):

    def __repr__(self): return self.url
    def __str__(self): return self.url
    def __iter__(self):
        for part in [self.scheme, self.host, 
        self.path, self.params, self.query, self.fragment]:
            yield part
        
    def __init__(self, url):
        self.new_url(url)

    def new_url(self, url):
        """ Assign a new url to this LazyUrl object """
        if is_lazyurl(url):
            self.url = url.url
        else:
            self.url = url
        self._delegate_parts(urlparse.urlparse(self.url))
        self._force_scheme()    
        self._update_url()

    # Getters / Setters
    def get_parts(self):
        return [p for p in self]
    
    def get_fullpath(self):
        """ the url without the shceme and host """
        return ''.join(self[2:])
    
    def set_scheme(self, scheme):
        """ Replace the scheme """
        self.scheme = scheme
        self._force_scheme()
        self._update_url()
        
    def set_host(self, host):
        """ Replace the host """
        self.host = host
        self._update_url()
        
    def set_path(self, path):
        """ Replace the path """
        if (path[0] is not '/'): path = '/' + path
        self.path = path.strip() # remove space
        self._update_url()
    

    #Internal Methods        
    def _delegate_parts(self, parsed_url):
        """ Delegate the split url """
        self.scheme = parsed_url.scheme
        if (not self.scheme):
            tmp = parsed_url.path.split('/')
            self.host = tmp[0]
            self.path = '/'.join(tmp[1:]) if (len(tmp) > 1) else '/'
        else:
            self.host = parsed_url.netloc        
            self.path = parsed_url.path or '/'
        self.query = parsed_url.query
        self.params = parsed_url.params
        self.fragment = parsed_url.fragment


    def _force_scheme(self):
        allowed_schemes = ['http', 'https', 'git', 'ftp']
        if self.scheme not in allowed_schemes:
            self.scheme = allowed_schemes[0]         

    def _update_url(self):
        self.url = urlparse.urlunparse(list(self))




def git_url(url):
    url = LazyUrl(url)
    url.set_scheme('git')
    return url

def https_url(url):
    url = LazyUrl(url)
    url.set_scheme('https')
    return url

def ftp_url(url):
    url = LazyUrl(url)
    url.set_scheme('ftp')
    return url


if __name__ == '__main__':
    
    url = 'stackoverflow.com/users/18865/gg'
    
    url = LazyUrl(url)
    print url.get_parts()
    print url
    
    #print url
    #url.set_path('user')
    #print url
        
    #print git_url(url)
    #print ftp_url(url)
    #print https_url(url)
    
    
