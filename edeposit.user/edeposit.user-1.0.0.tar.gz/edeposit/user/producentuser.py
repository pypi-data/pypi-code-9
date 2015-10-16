# -*- coding: utf-8 -*-
from plone.directives import form
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFDefault.exceptions import EmailAddressInvalid
from plone.dexterity.content import Container
from plone import api

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from Products.Five import BrowserView
import plone.app.users
from edeposit.user import MessageFactory as _
from zope.interface import invariant
from zope.interface.exceptions import Invalid

def checkEmailAddress(value):
    reg_tool = api.portal.get_tool(name='portal_registration')
    if value and reg_tool.isValidEmail(value):
        pass
    else:
        raise EmailAddressInvalid
    return True

                
# Interface class; used to define content-type schema.
class IProducentUserBasic(model.Schema, IImageScaleTraversable):
    """ a few fields from IProducentAdministrator """
    fullname = schema.TextLine(
        title=u"Jméno a příjmení",
        description=_(u'help_full_name_creation',
                      default=u"Enter full name, e.g. John Smith."),
        required=True)

    email = schema.ASCIILine(
        title=_(u'label_email', default=u'E-mail'),
        description=u'',
        required=True,
        constraint=checkEmailAddress)

    phone = schema.TextLine(
        title=_(u'label_phone', default=u'Telephone number'),
        description=_(u'help_phone',
                      default=u"Leave your phone number so we can reach you."),
        required=True,
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

    # @invariant
    # def checkPasswords(data):
    #     password, password_ctl = getattr(data,'password',None),getattr(data,'password_ctl',None)
    #     if password and password_ctl:
    #         if password != password_ctl:
    #             raise Invalid("hesla se musí shodovat")
    #     pass
        
    #     # raise Invalid(
    #     #     PC_("You cannot have a type as a secondary type without "
    #     #         "having it allowed. You have selected ${types}s.",
    #     #         mapping=dict(types=", ".join(missing))))
    #     # error_keys = [error.field_name for error in errors
    #     #               if hasattr(error, 'field_name')]
    #     # if not ('password' in error_keys or 'password_ctl' in error_keys):
    #     #     password = self.widgets['password'].getInputValue()
    #     #     password_ctl = self.widgets['password_ctl'].getInputValue()
    #     #     if password != password_ctl:
    #     #         err_str = _(u'Passwords do not match.')
    #     #         errors.append(WidgetInputError('password',
    #     #                                        u'label_password', err_str))
    #     #         errors.append(WidgetInputError('password_ctl',
    #     #                                        u'label_password', err_str))
    #     #         self.widgets['password'].error = err_str
    #     #         self.widgets['password_ctl'].error = err_str
    #     #         pass
    #     #         # Password field checked against RegistrationTool
    #     #         # Skip this check if password fields already have an error
    #     #         if not 'password' in error_keys:
    #     #             password = self.widgets['password'].getInputValue()
    #     #             if password:
    #     #                 # Use PAS to test validity
    #     #                 err_str = registration.testPasswordValidity(password)
    #     #                 if err_str:
    #     #                     errors.append(WidgetInputError('password',
    #     #                                                    u'label_password', err_str))
    #     #                     self.widgets['password'].error = err_str

    
class IProducentUser(IProducentUserBasic):
    """
    E-Deposit Producent User
    """
    """
    E-Deposit - Producent Administrator
    """
    form.fieldset(
        'personalinfo',
        label = _(u"Personal Info"),
        fields = ['fullname','email','phone']
        )

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
    #     title=u"Ulice a číslo",
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

    form.fieldset(
        'login',
        label = _(u"Login"),
        fields = ['username','password','password_ctl']
        )

    # username = schema.ASCIILine(
    #     title=_(u'label_user_name', default=u'User Name'),
    #     description=_(u'help_user_name_creation_casesensitive',
    #                   default=u"Enter a user name, usually something "
    #                   "like 'jsmith'. "
    #                   "No spaces or special characters. "
    #                   "Usernames and passwords are case sensitive, "
    #                   "make sure the caps lock key is not enabled. "
    #                   "This is the name used to log in."))
    
    # password = schema.Password(
    #     title=_(u'label_password', default=u'Password'),
    #     description=_(u'help_password_creation',
    #                   default=u'Enter your new password.'))
    
    # password_ctl = schema.Password(
    #     title=_(u'label_confirm_password',
    #             default=u'Confirm password'),
    #     description=_(u'help_confirm_password',
    #                   default=u"Re-enter the password. "
    #                   "Make sure the passwords are identical."))
    
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ProducentUser(Container):
    # Add your class methods and properties here
    pass


# View class
# The view is configured in configure.zcml. Edit there to change
# its public name. Unless changed, the view will be available
# TTW at content/@@sampleview

class SampleView(BrowserView):
    """ sample view class """
    # Add view methods here
