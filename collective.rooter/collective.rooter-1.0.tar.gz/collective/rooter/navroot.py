from threading import local


class NavigationRootInfo(local):
    root = None

_current_root = NavigationRootInfo()


def getNavigationRoot():
    """Get the current navigation root
    """
    return _current_root.root


def setNavigationRoot(root):
    """Set the current navigation root. This is normally done by an event
    subscriber during traversal.
    """
    _current_root.root = root
