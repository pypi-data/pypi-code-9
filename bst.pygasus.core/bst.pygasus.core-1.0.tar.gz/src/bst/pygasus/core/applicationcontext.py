from martian import baseclass
from grokcore.component import name
from grokcore.component import GlobalUtility

from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component.globalregistry import BaseGlobalComponents
from zope.component.globalregistry import GlobalAdapterRegistry

from bst.pygasus.core.interfaces import IApplicationContext
from bst.pygasus.core.interfaces import DEFAULT_EXTJS_APPLICATION


class LocalAdapterRegistry(GlobalAdapterRegistry):
    """ Local adapter/utilities registry
    """


class LocalComponentsRegistry(BaseGlobalComponents):
    """ The local component registry bound
        on application context.
    """
    def __init__(self, name):
        super(LocalComponentsRegistry, self).__init__(
            name=name,
            bases=(getGlobalSiteManager(),))

    def _init_registries(self):
        self.adapters = LocalAdapterRegistry(self, 'adapters')
        self.utilities = LocalAdapterRegistry(self, 'utilities')


@implementer(IApplicationContext)
class ApplicationContext(GlobalUtility):
    """ Represent a ExtJs Application. This is abstract
        class and need to subclass in your project.
    """
    baseclass()
    name(DEFAULT_EXTJS_APPLICATION)

    def __init__(self):
        super(ApplicationContext, self).__init__()
        self._sitemanager = LocalComponentsRegistry(self.application)

    def getSiteManager(self):
        return self._sitemanager

    def setSiteManager(self, sitemanager):
        self._sitemanager = sitemanager
