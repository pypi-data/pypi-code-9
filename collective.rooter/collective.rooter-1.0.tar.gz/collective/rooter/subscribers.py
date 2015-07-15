from collective.rooter.navroot import setNavigationRoot
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import adapter
from zope.publisher.interfaces import IEndRequestEvent
from zope.traversing.interfaces import IBeforeTraverseEvent


@adapter(INavigationRoot, IBeforeTraverseEvent)
def record_navigation_root(obj, event):
    """When traversing over a site manager that is a navigation root,
    record the navigation root in a thread-local.
    """
    setNavigationRoot(obj)


@adapter(IEndRequestEvent)
def clean_navigation_root(event):
    """When traversal is over, clear the navigation root thread-local
    """
    setNavigationRoot(None)
