from Products.CMFPlone.CatalogTool import CatalogTool
from collective.rooter.navroot import getNavigationRoot


# Make portal_catalog's search function use a navigation root if no path
# parameter is given
CatalogTool._oldSearchResults = CatalogTool.searchResults


def searchResults(self, REQUEST=None, **kw):
    if 'UID' not in kw\
            and 'path' not in kw\
            and (REQUEST is None or 'path' not in REQUEST):
        # Root catalog searches to the navigation root, except if path or UID
        # are explicitly given.
        root = getNavigationRoot()
        if root is not None:
            kw = kw.copy()
            kw['path'] = '/'.join(root.getPhysicalPath())
    return CatalogTool._oldSearchResults(self, REQUEST, **kw)
