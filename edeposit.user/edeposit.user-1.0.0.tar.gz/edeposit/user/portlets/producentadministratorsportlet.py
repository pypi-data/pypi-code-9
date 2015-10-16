from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

from edeposit.user import MessageFactory as _

class IProducentAdministratorsPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IProducentAdministratorsPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Producent Administrators Portlet")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('producentadministratorsportlet.pt')

    @property
    def administrators(self):
        ids = self.context.getAssignedProducentAdministrators() or []
        members = [ api.user.get(username = ii) for ii in ids]
        fullnames = [ mm.getProperty('fullname') for mm in members ]
        return [{'id':id,'fullname':fullname} for (id,fullname) in zip(ids,fullnames)]

    @property
    def editors(self):
        ids = self.context.getAssignedProducentEditors() or []
        members = [ api.user.get(username = ii) for ii in ids]
        fullnames = [ mm.getProperty('fullname') for mm in members ]
        return [{'id':id,'fullname':fullname} for (id,fullname) in zip(ids,fullnames)]

    @property
    def available(self):
        return self.context.portal_type=='edeposit.user.producent'

# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IProducentAdministratorsPortlet)

    def create(self, data):
        return Assignment(**data)

