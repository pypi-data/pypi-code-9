# -*- coding: utf-8 -*-
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from five import grok
from plone import api
from z3c.formwidget.query.interfaces import IQuerySource
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.namedfile.field import NamedBlobFile
from collections import namedtuple

from plone.supermodel import model
from Products.Five import BrowserView

from edeposit.user import MessageFactory as _
from edeposit.user.producentuser import IProducentUser
from edeposit.user.producentadministratorfolder import IProducentAdministratorFolder

from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from zope.interface import Invalid, Interface
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory

def checkEmailAddress(value):
    reg_tool = api.portal.get_tool(name='portal_registration')
    if value and reg_tool.isValidEmail(value):
        pass
    else:
        raise EmailAddressInvalid
    return True

# Interface class; used to define content-type schema.

class IProducentAdministrator(IProducentUser):
    """
    E-Deposit - Producent Administrator
    """
    # form.fieldset(
    #     'personalinfo',
    #     label = _(u"Personal Info"),
    #     fields = ['fullname','email','home_page','location','phone']
    #     )

    # fullname = schema.TextLine(
    #     title=_(u'label_full_name', default=u'Full Name'),
    #     description=_(u'help_full_name_creation',
    #                   default=u"Enter full name, e.g. John Smith."),
    #     required=False)

    # email = schema.ASCIILine(
    #     title=_(u'label_email', default=u'E-mail'),
    #     description=u'',
    #     required=True,
    #     constraint=checkEmailAddress)

    # home_page = schema.TextLine(
    #     title=_(u'label_homepage', default=u'Home page'),
    #     description=_(u'help_homepage',
    #                   default=u"The URL for your external home page, "
    #                   "if you have one."),
    #     required=False)

    # location = schema.TextLine(
    #     title=_(u'label_location', default=u'Location'),
    #     description=_(u'help_location',
    #                   default=u"Your location - either city and "
    #                   "country - or in a company setting, where "
    #                   "your office is located."),
    #     required=False)

    # phone = schema.TextLine(
    #     title=_(u'label_phone', default=u'Telephone number'),
    #     description=_(u'help_phone',
    #                   default=u"Leave your phone number so we can reach you."),
    #     required=False,
    #     )

    # form.fieldset(
    #     'address',
    #     label = _(u"Address"),
    #     fields = ['street','city','country']
    #     )
    # street = schema.TextLine(
    #     title=_(u'label_street', default=u'Street'),
    #     description=_(u'help_street',
    #                   default=u"Fill in the street and number."),
    #     required=False,
    #     )

    # city = schema.TextLine(
    #     title=_(u'label_city', default=u'City'),
    #     description=_(u'help_city',
    #                   default=u"Fill in the city you live in."),
    #     required=False,
    #     )

    # country = schema.TextLine(
    #     title=_(u'label_country', default=u'Country'),
    #     description=_(u'help_country',
    #                   default=u"Fill in the country you live in."),
    #     required=False,
    #     )
    # form.fieldset(
    #     'producent',
    #     label = _(u"Producent"),
    #     fields = ['producent',
    #               ]
    #     )

    # form.fieldset(
    #     'producent_info',
    #     label = _(u"Producent's Info"),
    #     fields = ['new_producent',
    #               'producent',
    #               'producent_title',
    #               'producent_home_page',
    #               'producent_location',
    #               'producent_contact',
    #               'producent_agreement',]
    #     )
    # form.fieldset(
    #     'producent_address',
    #     label = _(u"Producent's Address"),
    #     fields = [  'producent_street',
    #                 'producent_city',
    #                 'producent_country',
    #                 ]
    #     )
    # new_producent = schema.Bool(
    #     title=_(u'label_new_producent', default=u'New producent'),
    #     description=_(u'help_new_producent',
    #                   default=u"Do you wan to create new producent?"),
    #     required=False,
    #     )

    #form.widget(producent=AutocompleteFieldWidget)
    # producent = schema.Object(
    #     title=_(u'label_producent', default=u'Producent'),
    #     description=_(u'help_producent',
    #                   default=u"Fill in the producent you work for."),
    #     required=False,
    #     schema=IProducent
    #     )

    # producent_title = schema.TextLine(
    #     title=_(u'label_producent_title', default=u'Producent Title'),
    #     description=_(u'help_producent_title',
    #                   default=u"Enter full name of a producent."),
    #     required=True)

    # producent_home_page = schema.TextLine(
    #     title=_(u'label_producent_homepage', default=u'Home page of producent'),
    #     description=_(u'help_homepage',
    #                   default=u"The URL for a home page of your producent, "
    #                   "if he has one."),
    #     required=False)

    # producent_location = schema.TextLine(
    #     title=_(u'label_producent_location', default=u'Location'),
    #     description=_(u'help_producent_location',
    #                   default=u"Location of your producent - either city and "
    #                   "country - or in a company setting, where "
    #                   "your office is located."),
    #     required=False)

    # producent_street = schema.TextLine(
    #     title=_(u'label_producent_street', default=u'Street'),
    #     description=_(u'help_producent_street',
    #                   default=u"Fill in the street and number."),
    #     required=True,
    #     )

    # producent_city = schema.TextLine(
    #     title=_(u'label_producent_city', default=u'City'),
    #     description=_(u'help_producent_city',
    #                   default=u"Fill in the city your producent sits in."),
    #     required=True,
    #     )

    # producent_country = schema.TextLine(
    #     title=_(u'label_producent_country', default=u'Country'),
    #     description=_(u'help_producent_country',
    #                   default=u"Fill in the country your producent lives in."),
    #     required=True,
    #     )
    
    # producent_contact = schema.TextLine(
    #     title=_(u'label_producent_contact', default=u'Contact'),
    #     description=_(u'help_producent_contact',
    #                   default=u"Fill a phone, email or name of a person we can contact."),
    #     required=False)
    
    # producent_agreement = NamedBlobFile( title=_(u"Agreement with National Library Prague and producent"), 
    #                                      description=_(u"Fill in with signed agreement file."), 
    #                                      required=False )





# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ProducentAdministrator(Container):
    # Add your class methods and properties here
    pass

# View class
# The view is configured in configure.zcml. Edit there to change
# its public name. Unless changed, the view will be available
# TTW at content/@@sampleview

class SampleView(BrowserView):
    """ sample view class """
    # Add view methods here

class ProducentAdministratorAddForm(DefaultAddForm):
    portal_type="edeposit.user.producentadministrator"
    grok.context(IProducentAdministratorFolder)

    def add(self,object):
        if api.user.get(username=object.username):
            raise ActionExecutionError(Invalid(u"Uživatelské jméno již existuje. Na záložce Přihlášení použijte jiné."))
        if object.password != object.password_ctl:
            raise ActionExecutionError(Invalid(u"Hesla se neshodují. Na záložce Přihlášení zadejte hesla znovu."))
        return super(ProducentAdministratorAddForm,self).add(object)

class ProducentAdministratorAddView(DefaultAddView):
    form = ProducentAdministratorAddForm
    pass
