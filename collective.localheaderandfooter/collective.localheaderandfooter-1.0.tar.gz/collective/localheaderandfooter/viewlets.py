# -*- coding: utf-8 -*-

from datetime import date

from zope.dottedname.resolve import resolve
from zope.component import queryMultiAdapter

from plone.memoize import view
from plone.app.layout.viewlets import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from .utils import get_local_header
from .utils import get_local_footer


class HeaderViewlet(ViewletBase):
    """A simple viewlet which renders an header
    """

    dottedname = 'plone.app.layout.viewlets'
    default_template_name = 'portal_header.pt'
    default_view_name = 'default-portal-header'

    @property
    @view.memoize_contextless
    def default_path(self):
        mod = resolve(self.dottedname)
        path = '/'.join(
            mod.__path__ + [self.default_template_name]
        )
        return path

    @property
    def index(self):
        return ViewPageTemplateFile(self.default_path)

    def update(self):
        super(HeaderViewlet, self).update()
        self.local = self.get_local()

    def render(self):
        if self.local:
            return self.local
        # lookup for custom default views
        view = queryMultiAdapter((self.context, self.request),
                                 name=self.default_view_name)
        if view:
            return view()
        return self.index(self)

    @view.memoize
    def get_local(self):
        return get_local_header(self.context,
                                self.request)


class FooterViewlet(HeaderViewlet):
    """The footer viewlet
    """

    default_template_name = 'footer.pt'
    default_view_name = 'default-portal-footer'

    @property
    def year(self):
        # needed by default viewlet tmpl
        return date.today().year

    @view.memoize
    def get_local(self):
        return get_local_footer(self.context,
                                self.request)
