# -*- coding: utf-8 -*-
from zope.interface import Interface, implements, Invalid, invariant
from zope import schema

from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema

from Products.CMFDefault.exceptions import EmailAddressInvalid

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from five import grok
from .producent import IProducent
from plone import api
from z3c.formwidget.query.interfaces import IQuerySource
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.namedfile.field import NamedBlobFile
from collections import namedtuple

from edeposit.user import MessageFactory as _

class PasswordPairInvalid(schema.ValidationError):
    __doc__ = _(u'Passwords are not the same.')

def search_producents(query_string):
    portal_catalog = api.portal.get_tool('portal_catalog')
    brains = portal_catalog({'object_provides': IProducent.__identifier__})
    
        # Create a list of tuples (UID, Title) of results
    terms = [ SimpleTerm(value=brain['UID'], token=brain['UID'], title=brain['Title']) for brain in brains]
    return SimpleVocabulary(terms)

@grok.provider(IContextSourceBinder,IQuerySource)
def producent_source(context):
    """
    Populate vocabulary with values from portal_catalog.

    @param context: z3c.form.Form context object (in our case site root)

    @return: SimpleVocabulary containing all areas as terms.
    """
    # Acquire portal catalog
    portal_catalog = api.portal.get_tool(name='portal_catalog')
    brains = portal_catalog({'object_provides': IProducent.__identifier__})

    # Create a list of tuples (UID, Title) of results
    terms = [ SimpleTerm(value=brain['UID'], token=brain['UID'], title=brain['Title']) for brain in brains ]
    vocab = SimpleVocabulary(terms) 
    vocab.search = search_producents
    return vocab

producent_source.search = search_producents

def validateAccept(value):
    if not value == True:
        return False
    return True

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema

def checkEmailAddress(value):
    reg_tool = api.portal.get_tool(name='portal_registration')
    if value and reg_tool.isValidEmail(value):
        pass
    else:
        raise EmailAddressInvalid
    return True

class IEnhancedUserDataSchema(Interface):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    form.fieldset(
        'login',
        label = _(u"Login"),
        fields = ['username','password','password_ctl']
        )

    username = schema.ASCIILine(
        title=_(u'label_user_name', default=u'User Name'),
        description=_(u'help_user_name_creation_casesensitive',
                      default=u"Enter a user name, usually something "
                               "like 'jsmith'. "
                               "No spaces or special characters. "
                               "Usernames and passwords are case sensitive, "
                               "make sure the caps lock key is not enabled. "
                               "This is the name used to log in."))

    password = schema.Password(
        title=_(u'label_password', default=u'Password'),
        description=_(u'help_password_creation',
                      default=u'Enter your new password.'))

    password_ctl = schema.Password(
        title=_(u'label_confirm_password',
                default=u'Confirm password'),
        description=_(u'help_confirm_password',
                      default=u"Re-enter the password. "
                      "Make sure the passwords are identical."))
    @invariant
    def passwordsMatch(data):
        if data.password == data.password_ctl:
            return True
        raise PasswordPairInvalid
    
    form.fieldset(
        'personalinfo',
        label = _(u"Personal Info"),
        fields = ['fullname','email','home_page','location','phone']
        )

    fullname = schema.TextLine(
        title=_(u'label_full_name', default=u'Full Name'),
        description=_(u'help_full_name_creation',
                      default=u"Enter full name, e.g. John Smith."),
        required=False)

    email = schema.ASCIILine(
        title=_(u'label_email', default=u'E-mail'),
        description=u'',
        required=True,
        constraint=checkEmailAddress)

    home_page = schema.TextLine(
        title=_(u'label_homepage', default=u'Home page'),
        description=_(u'help_homepage',
                      default=u"The URL for your external home page, "
                      "if you have one."),
        required=False)

    location = schema.TextLine(
        title=_(u'label_location', default=u'Location'),
        description=_(u'help_location',
                      default=u"Your location - either city and "
                      "country - or in a company setting, where "
                      "your office is located."),
        required=False)

    phone = schema.TextLine(
        title=_(u'label_phone', default=u'Telephone number'),
        description=_(u'help_phone',
                      default=u"Leave your phone number so we can reach you."),
        required=False,
        )

    form.fieldset(
        'address',
        label = _(u"Address"),
        fields = ['street','city','country']
        )
    street = schema.TextLine(
        title=_(u'label_street', default=u'Street'),
        description=_(u'help_street',
                      default=u"Fill in the street and number."),
        required=False,
        )

    city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        description=_(u'help_city',
                      default=u"Fill in the city you live in."),
        required=False,
        )

    country = schema.TextLine(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country',
                      default=u"Fill in the country you live in."),
        required=False,
        )
    form.fieldset(
        'producent',
        label = _(u"Producent"),
        fields = ['producent',
                  ]
        )

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
    producent = schema.Choice(
        title=_(u'label_producent', default=u'Producent'),
        description=_(u'help_producent',
                      default=u"Fill in the producent you work for."),
        required=False,
        source=producent_source,
        )

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




class EnhancedUserData(namedtuple("EnhancedUser",
                                  ['username','password','password_ctl',
                                   'fullname','email','home_page',
                                   'location','phone','street',
                                   'city','country',
                                   'producent',
                                   # 'producent_title',
                                   # 'producent_home_page',
                                   # 'producent_location',
                                   # 'producent_contact',
                                   # 'producent_street',
                                   # 'producent_city',
                                   # 'producent_country',
                                   # 'producent_agreement',
                                   ])):
    implements(IEnhancedUserDataSchema)

