from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter

try:
    from collective.lineage.interfaces import IChildSite
except ImportError:
    IChildSite = None


class SiteLogoUtilsView(BrowserView):

    @property
    def controlpanel_url(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u"plone_portal_state")
        root = portal_state.navigation_root()
        if IChildSite and not IChildSite.providedBy(root):
            root = portal_state.portal()
        return '{0}/@@sitelogo-controlpanel'.format(root.absolute_url())
