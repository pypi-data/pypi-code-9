# -*- coding: utf-8 -*-
from zope import schema
import zope
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.z3cform.templates import ZopeTwoFormTemplateFactory
import plone.app.users.browser.register
from zope.publisher.browser import BrowserView
from z3c.form.browser.radio import RadioFieldWidget
from plone.directives import form
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.navigation.interfaces import INavigationRoot
from z3c.form import field, button, validator
from plone import api
from zope.interface import Invalid, Interface
from edeposit.user import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import adapts
from zope.component import getUtility
from zope.component import queryUtility
from plone.z3cform.fieldsets import extensible
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from edeposit.user.producent import IProducent
from edeposit.user.producentuser import IProducentUser
from edeposit.user.producenteditor import IProducentEditor, ProducentEditor
from edeposit.user.producentfolder import IProducentFolder
from edeposit.user.producentadministrator import IProducentAdministrator, ProducentAdministrator
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory, IValidator, IErrorViewSnippet
import os.path
import logging
import string
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
from plone.i18n.normalizer.interfaces import IURLNormalizer, IIDNormalizer
from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.supermodel import model
from plone.dexterity.utils import getAdditionalSchemata
from Acquisition import aq_inner, aq_base
from Products.CMFDefault.exceptions import EmailAddressInvalid
from zope.interface import invariant, Invalid
from itertools import chain
from five import grok
import re

# Logger output for this module
logger = logging.getLogger(__name__)

class IProducentAdministrators(model.Schema):
    administrators = zope.schema.List(
        title = _(u'Producent Administrators'),
        description = u'Přidejte alespoň jednoho administrátora',
        required = True,
        value_type = zope.schema.Object( title=_('Producent Administrator'), schema=IProducentAdministrator ),
        unique = False,
        min_length = 1,
    )

class IAdministrator(model.Schema):
    administrator = zope.schema.Object(
        title = _(u'Producent Administrator'),
        description = u"správce přidává editory, upravuje informace o producentovi.",
        required = True,
        schema=IProducentAdministrator,
    )

def checkEmailAddress(value):
    reg_tool = api.portal.get_tool(name='portal_registration')
    if value and reg_tool.isValidEmail(value):
        return True
    else:
        raise EmailAddressInvalid()
    return False

def checkForRegularTextFactory(regex):
    def validator(value):
        return re.search(regex,value)
    return validator

# Interface class; used to define content-type schema.
class IEditor(model.Schema):
    """ a few fields from IProducentAdministrator """
    model.fieldset('editor',
                   label = _(u'Producent Editor'),
                   fields = ['fullname',
                             'email',
                             'phone',
                             'username',
                             'password',
                             'password_ctl',
                         ]
    )

    fullname = schema.TextLine(
        title=u"Jméno a příjmení",
        description=_(u'help_full_name_creation',
                      default=u"Enter full name, e.g. John Smith."),
        required=False)

    email = schema.ASCIILine(
        title=_(u'label_email', default=u'E-mail'),
        description=u'',
        constraint = checkEmailAddress,
        required=False,
    )

    phone = schema.ASCIILine(
        title=_(u'label_phone', default=u'Telephone number'),
        description=_(u'help_phone',
                      default=u"Leave your phone number so we can reach you."),
        required=False,
        constraint = checkForRegularTextFactory(r'^[ 0-9\+]*$'),
    )
    
    username = schema.ASCIILine(
        title=_(u'label_user_name', default=u'User Name'),
        description=_(u'help_user_name_creation_casesensitive',
                      default=u"Enter a user name, usually something "
                      "like 'jsmith'. "
                      "No spaces or special characters. "
                      "Usernames and passwords are case sensitive, "
                      "make sure the caps lock key is not enabled. "
                      "This is the name used to log in."),
        required=False,
        constraint = checkForRegularTextFactory(r'^[a-z0-9_\.A-Z]{5,32}$'),
    )
    
    password = schema.Password(
        title=_(u'label_password', default=u'Password'),
        description=_(u'help_password_creation',
                      default=u'Enter your new password.'),
        required=False,
    )
    
    password_ctl = schema.Password(
        title=_(u'label_confirm_password',
                default=u'Confirm password'),
        description=_(u'help_confirm_password',
                      default=u"Re-enter the password. "
                      "Make sure the passwords are identical."),
        required=False,
    )


class ProducentAddForm(DefaultAddForm):
    label = _(u"Registration of a producent")
    description = _(u"Please fill informations about user and producent.")
    default_fieldset_label = u"Producent"
    enable_form_tabbing = False
    @property
    def additionalSchemata(self):
        schemata =       [IAdministrator,] +\
                         [IEditor,] +\
                         [s for s in getAdditionalSchemata(portal_type=self.portal_type)]
        return schemata

    def updateWidgets(self):
        super(ProducentAddForm, self).updateWidgets()
        self.widgets['IBasic.title'].label=u"Název producenta"

    def getProducentsFolder(self):
        return self.context

    def extractData(self):
        data, errors = super(ProducentAddForm,self).extractData()
        return data, errors

    @button.buttonAndHandler(_(u"Register"))
    def handleRegister(self, action):
        print "handle registrer"
        data, errors = self.extractData()
        if errors:
            print "all errors views names", map(lambda err: err.widget.name, errors)
            print self.formErrorsMessage
            print "self.widgets.errors", self.widgets.errors
            self.status = self.formErrorsMessage
            return

        administrator = data['IAdministrator.administrator']
        if api.user.get(username=administrator.username):
            raise ActionExecutionError(Invalid(u"Uživatelské jméno u správce producenta je již použito. Vyplňte jiné."))   
        # check administrator passwords
        if administrator.password_ctl != administrator.password:
            raise ActionExecutionError(Invalid(u"U správce producenta se neshodují zadaná hesla. Vyplňte hesla znovu."))

        editorFields = ['fullname','email','phone','username','password','password_ctl']
        editorValues = map(lambda key: data.get('IEditor.'+key,None), editorFields)

        if filter(lambda value: value, editorValues):
            if False in map(lambda value: bool(value), editorValues):
                raise ActionExecutionError(Invalid(u"Některé položky u editora nejsou vyplněny. Buď vyplňte editorovi všechny položky, nebo je všechny smažte."))
                
            editorData = dict(zip(editorFields, editorValues))
            if editorData['password'] != editorData['password_ctl']:
                raise ActionExecutionError(Invalid(u"U editora se neshodují zadaná hesla. Vyplňte hesla znovu."))
            if api.user.get(username=editorData['username']):
                raise ActionExecutionError(Invalid(u"Uživatelské jméno u editora je již obsazené. Vyplňte jiné."))

        producentsFolder = self.getProducentsFolder()
        # hack for title and description
        data['title'] = data.get('IBasic.title','')
        data['description'] = data.get('IBasic.description','')

        producent = createContentInContainer(producentsFolder, "edeposit.user.producent", **data)

        if filter(lambda value: value, editorValues):
            editorsFolder = producent['producent-editors']
            editorData['title'] = editorData['fullname']
            editor = createContentInContainer(editorsFolder, "edeposit.user.producenteditor", **editorData)


        administratorsFolder = producent['producent-administrators']
        

        administrator.title = getattr(administrator,'fullname',None)
        addContentToContainer(administratorsFolder, administrator, False)

        if producent is not None:
            wft = api.portal.get_tool('portal_workflow')
            wft.doActionFor(producent,'submit')
            # mark only as finished if we get the new object
            self._finishedAdd = True
            IStatusMessage(self.request).addStatusMessage(_(u"Item created"), "info")
            url = "%s/%s" % (api.portal.getSite().absolute_url(), 'register-with-producent-successed')
            self.request.response.redirect(url)
    pass

class ProducentAddView(DefaultAddView):
    form = ProducentAddForm

class PostLoginView(BrowserView):
    def update(self):
        portal = api.portal.get()
        dashboard_url = os.path.join(portal.absolute_url(),'producents')
        return self.request.redirect(dashboard_url)

class RegisteredView(BrowserView):
    pass

class ProducentAdministratorFactory(object):
    zope.interface.implements(IObjectFactory)
    adapts(Interface, Interface, Interface, Interface)
    
    def __init__(self, context, request, form, widget):
        self.context = context
        self.request = request
        self.form = form
        self.widget = widget

    def __call__(self, value):
        created=createContent('edeposit.user.producentadministrator',**value)
        return created

class ProducentEditorFactory(object):
    zope.interface.implements(IObjectFactory)
    adapts(Interface, Interface, Interface, Interface)
    
    def __init__(self, context, request, form, widget):
        self.context = context
        self.request = request
        self.form = form
        self.widget = widget

    def __call__(self, value):
        print "producent editor factory", value
        created=createContent('edeposit.user.producenteditor',**value)
        return created

class IProducentWithAdministrators(IProducent):
    administrators = zope.schema.List(
        title = _(u'Producent Administrators'),
        description = _(u'Fill in at least one producent administrator'),
        required = True,
        value_type = zope.schema.Object( title=_('Producent Administrator'), schema=IProducentAdministrator ),
        unique = False
    )

def normalizeTitle(title):
    title = u"Cosi českého a. neobratného"
    util = queryUtility(IIDNormalizer)
    result = util.normalize(title)
    return result


class RegistrationForm(ProducentAddForm):
    portal_type = 'edeposit.user.producent'
    template = ViewPageTemplateFile('form.pt')

    def getProducentsFolder(self):
        portal = api.portal.get()
        return portal['producents']


class IRegistrationAtOnce(form.Schema):
    producent_name = schema.TextLine (
        title = u"Firma / Jméno, příjmení",
        required = True)

    pravni_forma = schema.TextLine (
        title = u"Právní forma",
        required = True)

    domicile = schema.TextLine (
        title = u"Sídlo (celá adresa)",
        required = False )

    ico = schema.ASCIILine (
        title = u"IČ",
        constraint = checkForRegularTextFactory(r'^[a-zA-Z 0-9\+]*$'),
        required = False )

    dic = schema.ASCIILine (
        title = u"DIČ",
        constraint = checkForRegularTextFactory(r'^[a-zA-Z 0-9\+]*$'),
        required = False )

    zastoupen = schema.TextLine (
        title = u"Statutární zástupce organizace",
        required = False )

    form.fieldset('producent_administrator',
                  label = u"Správce producenta",
                  fields = ('administrator_fullname',
                            'administrator_email',
                            'administrator_phone',
                            'administrator_username',
                            'administrator_password',
                            'administrator_password_ctl',
                            )
        )
    
    administrator_fullname = schema.TextLine (
        title = u"Jméno a příjmení",
        required = True )

    administrator_email = schema.ASCIILine (
        title = u"email",
        constraint = checkEmailAddress,
        required = True )

    administrator_phone = schema.ASCIILine (
        title = u"Telefonní číslo",
        constraint = checkForRegularTextFactory(r'^[ 0-9\+]*$'),
        required = True )

    administrator_username = schema.ASCIILine (
        title = u"Uživatelské jméno",
        constraint = checkForRegularTextFactory(r'^[a-z0-9_\.A-Z]{5,32}$'),
        required = True )

    administrator_password = schema.Password (
        title = u"Heslo",
        required = True )

    administrator_password_ctl = schema.Password (
        title = u"Potvrďte heslo",
        required = True )

    form.fieldset('producent_editor',
                  label = u"Editor producenta",
                  fields = ('editor_fullname',
                            'editor_email',
                            'editor_phone',
                            'editor_username',
                            'editor_password',
                            'editor_password_ctl',
                            )
        )
    
    editor_fullname = schema.TextLine (
        title = u"Jméno a příjmení",
        required = False )

    editor_email = schema.ASCIILine (
        title = u"email",
        constraint = checkEmailAddress,
        required = False )

    editor_phone = schema.ASCIILine (
        title = u"Telefonní číslo",
        constraint = checkForRegularTextFactory(r'^[ 0-9\+]*$'),
        required = False )

    editor_username = schema.ASCIILine (
        title = u"Uživatelské jméno",
        constraint = checkForRegularTextFactory(r'^[a-z0-9_\.A-Z]{5,32}$'),
        required = False )

    editor_password = schema.Password (
        title = u"Heslo",
        required = False )

    editor_password_ctl = schema.Password (
        title = u"Potvrďte heslo",
        required = False )
    

class RegistrationAtOnceForm(form.SchemaForm):
    schema = IRegistrationAtOnce
    default_fieldset_label = u"Producent"
    label = u"Registrace producenta"
    description = u"""<p>Vyplněním těchto údajů získáte přístup k aplikaci Národní knihovny, která umožňuje ukládání vašich elektronických publikací, jejich dlouhodobou ochranu a šíření podle Vašich instrukcí.</p>
<p>Pro využívání základních funkcí systému postačí vyplnit tento online formulář. Dalším krokem je uzavření písemné smlouvy, která umožní další funkčnosti včetně řízené distribuce vašich e-publikací.</p>"""

    ignoreContext = True
    enableCSRFProtection = True
    enable_form_tabbing = False

    def extractData(self):
        def getErrorView(widget,error):
            view = zope.component.getMultiAdapter( (error, 
                                                    self.request, 
                                                    widget, 
                                                    widget.field, 
                                                    widget.form, 
                                                    self.context), 
                                                   IErrorViewSnippet)
            view.update()
            widget.error = view
            return view

        data, errors = super(RegistrationAtOnceForm,self).extractData()

        reg_tool = api.portal.get_tool(name='portal_registration')
        
        widgets = self.groups[0].widgets
        username = data.get('administrator_username')
        if username:
            if api.user.get(username = username):
                errors += (getErrorView(widgets.get('administrator_username'),
                                        Invalid(u"Uživatelské jméno je již použito. Vyplňte jiné.")),)
                pass
            
        pwd1 = data.get('administrator_password')
        pwd2 = data.get('administrator_password_ctl')
        if pwd1 and len(pwd1) < 5:
            errors += (getErrorView(widgets.get('administrator_password'), 
                                    Invalid(u"Heslo je krátké. Nejméně 5 znaků.")),)
        if pwd2 and len(pwd2) < 5:
            errors += (getErrorView(widgets.get('administrator_password_ctl'), 
                                    Invalid(u"Heslo je krátké. Nejméně 5 znaků.")),)
        if (pwd1 and pwd2) and (len(pwd1) >= 5 and len(pwd2) >= 5) and  (pwd1 != pwd2):
            errors += (getErrorView(widgets.get('administrator_password'),  Invalid(u"Hesla se neshodují.")),)
            errors += (getErrorView(widgets.get('administrator_password_ctl'),  Invalid(u"Hesla se neshodují.")),)

        email = data.get('administrator_email')
        if email and not reg_tool.isValidEmail(email):
            errors += (getErrorView(widgets.get('administrator_email'),  Invalid(u"Toto není platný email.")),)

        widgets = self.groups[1].widgets
        username = data.get('editor_username')
        if username:
            if api.user.get(username = username):
                errors += (getErrorView(widgets.get('editor_username'),
                                        Invalid(u"Uživatelské jméno je již použito. Vyplňte jiné.")),)
                pass
            
        pwd1 = data.get('editor_password')
        pwd2 = data.get('editor_password_ctl')
        if pwd1 and len(pwd1) < 5:
            errors += (getErrorView(widgets.get('editor_password'), 
                                    Invalid(u"Heslo je krátké. Nejméně 5 znaků.")),)
        if pwd2 and len(pwd2) < 5:
            errors += (getErrorView(widgets.get('editor_password_ctl'), 
                                    Invalid(u"Heslo je krátké. Nejméně 5 znaků.")),)

        if (pwd1 and pwd2) and (len(pwd1) >= 5 and len(pwd2) >= 5) and (pwd1 != pwd2):
            errors += (getErrorView(widgets.get('editor_password'),  Invalid(u"Hesla se neshodují.")),)
            errors += (getErrorView(widgets.get('editor_password_ctl'),  Invalid(u"Hesla se neshodují.")),)

        email = data.get('editor_email')
        if email and not reg_tool.isValidEmail(email):
            errors += (getErrorView(widgets.get('editor_email'),  Invalid(u"Toto není platný email.")),)

        return (data,errors)


    @button.buttonAndHandler(_(u"Register"))
    def handleRegister(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # zkontrolujeme editora, jesli je neco vyplnene
        editorKeys = [ key for key in data.keys() if key.startswith('editor_') ]
        definedEditorKeys = [ key for key in IRegistrationAtOnce.names() if key.startswith('editor_')]

        if True in [ bool(data[key]) for key in editorKeys]:
            if frozenset(editorKeys) != frozenset(definedEditorKeys):
                raise ActionExecutionError(Invalid(u"Pokud chcete editora, vyplňte všechna jeho políčka."))

            if False in [ bool(data[key]) for key in editorKeys ]:
                raise ActionExecutionError(Invalid(u"Pokud chcete editora, vyplňte všechna jeho políčka."))
            pass

        producentData = dict(zip( ('title','pravni_forma','domicile','ico','dic', 'zastoupen'), 
                                  map(data.__getitem__,('producent_name','pravni_forma','domicile','ico','dic','zastoupen'))))
        producents = api.portal.get()['producents']
        newProducent = createContentInContainer(producents,'edeposit.user.producent',**producentData)

        # username, email, password, properties
        def createUser(data,prefix=""):
            userFields = ('username','password','email')
            kwargs = dict(zip(userFields,map(data.__getitem__, map(prefix.__add__,userFields))))
            propertyFields = ('phone','fullname')
            properties = dict(zip(propertyFields, map(data.__getitem__, map(prefix.__add__, propertyFields))))
            newUser = api.user.create(properties = properties, **kwargs)
            return newUser

        newUser = createUser(data, prefix = "administrator_")

        api.group.add_user(groupname="Producent Editors", username=newUser.id )
        api.group.add_user(groupname="Producent Contributors", username=newUser.id )
        api.group.add_user(groupname="Producent Administrators", username=newUser.id )

        api.user.grant_roles(username=newUser.id,  obj=newProducent,
                             roles=('E-Deposit: Producent Member',
                                    'E-Deposit: Producent Editor',
                                    'E-Deposit: Producent Administrator',
                                    'Editor','Reader'))
        api.user.grant_roles(username=newUser.id,  obj = newProducent['epublications'],
                             roles=('E-Deposit: Producent Member',
                                    'E-Deposit: Producent Editor',
                                    'E-Deposit: Producent Administrator',
                                    'Contributor'))
        
        if True in [ bool(data[key]) for key in editorKeys ]:
            newUser = createUser(data,prefix="editor_")
            api.group.add_user(groupname="Producent Editors", username=newUser.id )
            api.group.add_user(groupname="Producent Contributors", username=newUser.id )
            api.user.grant_roles(username=newUser.id,
                                 obj = newProducent['epublications'],
                                 roles=('E-Deposit: Producent Member',
                                        'E-Deposit: Producent Editor',
                                        'Contributor'))
            api.user.grant_roles(username=newUser.id, obj=newProducent,
                                 roles=('E-Deposit: Producent Member',
                                        'E-Deposit: Producent Editor', 
                                        'Reader'))
        
        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor(newProducent,'submit')
        
        with api.env.adopt_roles(roles=["E-Deposit: Acquisitor",]):
            wft.doActionFor(newProducent,'approve')
            #wft.doActionFor(newProducent,'generateAgreement')

        IStatusMessage(self.request).addStatusMessage(u"Registrace proběhla úspěšně", "info")
        url = "%s/%s" % (api.portal.getSite().absolute_url(), 'register-with-producent-successed')
        self.request.response.redirect(url)

