from time import time
from urllib.parse import urljoin
from urllib.parse import urlparse

from grokcore import component
from zope.interface import implementer
from zope.component import queryUtility
from bst.pygasus.core.interfaces import IBaseUrl
from bst.pygasus.wsgi.interfaces import IRequest
from bst.pygasus.core.interfaces import IApplicationContext
from bst.pygasus.core.interfaces import DEFAULT_EXTJS_APPLICATION

X_FULL_PATH = 'X_FULL_PATH'


class ramcache(object):
    """ decorator to cache a function into ram
        arguments should be hashable
    """

    def __init__(self, expire):
        """ expire in miliseconds
        """
        self.expire = expire
        self.cache = dict()

    def __call__(self, func):
        def wrapper(*args, **kw):
            key = hash((args, tuple(kw),))
            cache = self.cache.setdefault(key, dict(last=0,
                                                    result=None))
            if cache['last'] + self.expire < time():
                cache['last'] = time()
                r = func(*args, **kw)
                cache['result'] = r
                return r
            else:
                return cache['result']
        return wrapper


@implementer(IBaseUrl)
class BaseUrl(component.Adapter):
    component.context(IRequest)

    def __init__(self, request):
        self.request = request

    def url(self, relativ_path=None):
        if X_FULL_PATH in self.request.headers:
            base_url = self.request.headers.get(X_FULL_PATH)
        else:
            base_url = self.request.application_url

        if not base_url.endswith('/'):
            base_url = '%s/' % base_url

        # if the publisher take a default utility. we
        # need rebuild the correct url.
        appname = urlparse(base_url).path.split('/')[-2:-1][0]
        if queryUtility(IApplicationContext, name=appname) is None:
            base_url = '%s%s/' % (base_url, DEFAULT_EXTJS_APPLICATION,)

        if relativ_path is None:
            return base_url

        if relativ_path.startswith('/'):
            relativ_path = relativ_path[1:]

        return base_url + relativ_path
