from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.portlet.fullview import msgFact as _
from collective.portlet.fullview import msgFactPlone as _p
from plone.app.portlets.browser import z3cformhelper
from plone.app.portlets.portlets import base
from plone.app.uuid.utils import uuidToCatalogBrain
from plone.app.uuid.utils import uuidToObject
from plone.app.vocabularies.catalog import CatalogSource
from plone.memoize import ram
from plone.portlets.interfaces import IPortletDataProvider
from z3c.form import field
from zope import schema
from zope.i18n import translate
from zope.interface import implements
from zope.globalrequest import getRequest
from zope.publisher.interfaces.browser import IBrowserView
import time


class IFullViewPortlet(IPortletDataProvider):

    content_uid = schema.Choice(
        title=_(u'label_content_uid', default=u'Content Item'),
        description=_(
            u'help_content_uid',
            default=u'The content object to display in the portlet.'
        ),
        required=True,
        source=CatalogSource(),
    )

    show_title = schema.Bool(
        title=_(u"label_show_title", default=u"Show Content Title"),
        description=_(
            u"help_show_title",
            default=u"Show the content title."),
        default=True,
        required=False
    )

    link_title = schema.Bool(
        title=_(u"label_link_title", default=u"Link Content Title"),
        description=_(
            u"help_link_title",
            default=u"Link the content title with the content."),
        default=True,
        required=False
    )

    show_content = schema.Bool(
        title=_(u"label_show_content", default=u"Show content"),
        description=_(
            u"help_show_content",
            default=u"Show the content. You might want to not show it, if you "
                    "only want to show title and description and link to the "
                    "content."),
        default=True,
        required=False
    )

    omit_border = schema.Bool(
        title=_p(u"Omit portlet border"),
        description=_p(u"Tick this box if you want to render the text above "
                       u"without the standard header, border or footer."),
        required=False,
        default=False
    )


class Assignment(base.Assignment):
    implements(IFullViewPortlet)
    content_uid = None
    show_title = True
    link_title = True
    show_content = True
    omit_border = False

    def __init__(self, content_uid, show_title, link_title, show_content,
                 omit_border):
        self.content_uid = content_uid
        self.show_title = show_title
        self.link_title = link_title
        self.show_content = show_content
        self.omit_border = omit_border

    @property
    def portlet_id(self):
        """Return the portlet assignment's unique object id.
        """
        return id(self)

    @property
    def title(self):
        """Title of add view in portlet management screen."""
        item_title = u"Full View Portlet"
        if self.content_uid:
            item = uuidToCatalogBrain(self.content_uid)
            if item:
                item_title = safe_unicode(item.Title)
        request = getRequest()
        return u"{0}{1}{2}".format(
            translate(_(u"Full View Portlet"), context=request),
            " - " if item_title else "",
            item_title
        )


def _render_cachekey(method, self):
    context = aq_inner(self.context)
    timeout = time.time() // (60 * 60)  # cache for 60 min
    portal_membership = getToolByName(context, 'portal_membership')
    ctx = self.fullview_context
    return (
        self.data.portlet_id,
        '/'.join(ctx.getPhysicalPath()),
        ctx.modification_date.ISO(),
        portal_membership.getAuthenticatedMember().id,
        timeout
    )


class Renderer(base.Renderer):

    @property
    def fullview_context(self):
        item = uuidToObject(self.data.content_uid)
        return item

    def available(self):
        """Only render the portlet once.
        Avoids infinite recursion, when viewing a derived fullview portlet in
        the same path as the context which is shown in the fullview portlet is
        located.
        """
        portlet_id = self.data.portlet_id
        if portlet_id is None:
            # E.g. for collective.panels, where no portlet hashes are
            # available. Just return True, as these portlets are not inherited
            # anyways.
            return True

        if self.request.get('portlet_rendered_{0}'.format(portlet_id), False):
            return False
        self.request.set('portlet_rendered_{0}'.format(portlet_id), True)
        return True

    @ram.cache(_render_cachekey)
    def render(self):
        return self._template()

    _template = ViewPageTemplateFile('fullview.pt')


class AddForm(z3cformhelper.AddForm):
    fields = field.Fields(IFullViewPortlet)
    label = _(u"Add Full View Portlet")
    description = _(u"Show a content item as full view.")

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):
    fields = field.Fields(IFullViewPortlet)
    label = _(u"Edit Full View Portlet")
    description = _(u"Show a content item as full view.")


class FullViewItem(BrowserView):

    def __init__(self, context, request):
        super(FullViewItem, self).__init__(context, request)
        self.item_type = self.context.portal_type

    @property
    def default_view(self):
        context = self.context
        item_layout = context.getLayout()
        default_view = context.restrictedTraverse(item_layout)
        return default_view

    @property
    def item_macros(self):
        default_view = self.default_view
        if IBrowserView.providedBy(default_view):
            # IBrowserView
            return default_view.index.macros
        else:
            # FSPageTemplate
            return default_view.macros

    @property
    def item_url(self):
        context = self.context
        url = context.absolute_url()
        props = getToolByName(context, 'portal_properties')
        use_view_action = props.site_properties.typesUseViewActionInListings
        return self.item_type in use_view_action and '%s/view' % url or url
