from zope import schema
from zope.interface import Interface
from zope.interface import Attribute
from zope.component.interfaces import ISite

# main name for application context
DEFAULT_EXTJS_APPLICATION = 'mainapp'


class IApplicationContext(ISite):
    title = Attribute('title of application')
    resources = Attribute('fanstatic resources for all js and css')
    application = Attribute('classname of application entry point eg. "bielbienne.iptt.Application"')
    namespace = Attribute('Extjs name space eg: "bielbienne.iptt"')

    credentials_pluggins = Attribute('a list of utility names for credentials plugins')
    authentication_pluggins = Attribute('a list of utility names auth plugins')


class IBaseUrl(Interface):

    def __init__(self, request):
        """
            request: Client Request
        """

    def url(self, relativ_path=None):
        """ return base url or a url build
            with a given relative path
        """
