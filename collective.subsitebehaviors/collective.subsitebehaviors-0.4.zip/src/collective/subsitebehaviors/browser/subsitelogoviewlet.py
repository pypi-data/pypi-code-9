from Acquisition import aq_acquire
import plone.api as api
from plone.app.layout.viewlets.common import LogoViewlet
from plone.app.layout.navigation.root import getNavigationRoot
from borg.localrole.interfaces import IFactoryTempFolder
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.interfaces._content import IContentish

from collective.subsitebehaviors.behaviors import ISubSite


class SubsiteLogoViewlet(LogoViewlet):
    index = ViewPageTemplateFile('subsitelogoviewlet.pt')

    def __init__(self, context, request, view, manager=None):
        super(SubsiteLogoViewlet, self).__init__(context, request, view, manager)
        self.subsitelogo = False
        self.logo_tag = None

    def update(self):

        nav_root = api.portal.get_navigation_root(context=self.context)

        if ISubSite.providedBy(nav_root) and getattr(nav_root, 'logoImage'):
            self.subsitelogo = True
            scales = api.content.get_view("images", nav_root, self.request)
            scale = scales.scale("logoImage", "logo")
            self.logo_tag = scale.tag() if scale else scales.tag("logoImage")
        else:
           self.subsitelogo = False
           super(SubsiteLogoViewlet, self).update()

