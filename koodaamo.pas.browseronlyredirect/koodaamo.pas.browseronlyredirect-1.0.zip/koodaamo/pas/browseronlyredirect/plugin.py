"""Class: BrowseronlyredirectHelper"""

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from Products.PluggableAuthService.plugins.CookieAuthHelper import CookieAuthHelper


class BrowseronlyredirectHelper(CookieAuthHelper):
    "replacement that only redirects if the user agent is a browser"

    meta_type = 'Browser-only-redirecting Cookie Auth Helper'
    security = ClassSecurityInfo()

    def __init__( self, id, title=None ):
        self._setId( id )
        self.title = title

    security.declarePrivate('challenge')
    def challenge(self, request, response, **kw):
        "Challenge the user for credentials but only if the UA is a real boy"
        if request["HTTP_USER_AGENT"][:5] in ("Mozil", "Lynx/", "Webki", "Opera"):
            return self.unauthorized()
        else:
            return 0

InitializeClass(BrowseronlyredirectHelper)
