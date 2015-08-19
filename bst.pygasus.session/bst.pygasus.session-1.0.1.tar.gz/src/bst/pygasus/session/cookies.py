import random
import string

from bst.pygasus.core import ext
from bst.pygasus.session.interfaces import IClientIdentification


COOKIE_SESSION_LENGHT = 100
COOKIE_SESSION_KEY = 'pygasus_session'


class CookieClientIdentification(ext.Adapter):
    ext.context(ext.IRequest)
    ext.implements(IClientIdentification)

    def __init__(self, request):
        self.request = request

    def identification(self):
        """ cookie expiration will do on server. BE SURE A OLD COOKIE
            WILL BE OVERIDE AFTER HIS LIVE TIME!
        """
        return self.request.cookies.get(COOKIE_SESSION_KEY)

    def apply(self, secure=False):
        """ the secure flag means that this
            cookie can be set on http and https.
        """
        cookie = self.genereate_id()
        self.request.cookies[COOKIE_SESSION_KEY] = cookie
        self.request.response.set_cookie(key=COOKIE_SESSION_KEY,
                                         value=cookie,
                                         secure=secure)
        return cookie

    def genereate_id(self):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(COOKIE_SESSION_LENGHT))
