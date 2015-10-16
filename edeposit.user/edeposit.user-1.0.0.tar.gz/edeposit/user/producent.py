# -*- coding: utf-8 -*-
from z3c.form import group, field, button
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.app.textfield import RichText
from plone.directives import dexterity, form
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.app.form.widgets import MultiCheckBoxWidget
from plone.supermodel import model
from Products.Five import BrowserView
from five import grok
from plone.app.vocabularies import users
from edeposit.user import MessageFactory as _
from plone import api
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.interface import implements
from zope.component import adapts, getMultiAdapter
from Products.statusmessages.interfaces import IStatusMessage

from plone.namedfile.interfaces import INamedBlobFileField, INamedBlobImageField
from plone.namedfile.interfaces import INamedBlobFile, INamedBlobImage
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory, IValidator, IErrorViewSnippet
from operator import ne, is_not
from functools import partial
from string import Template
from collections import defaultdict

# Interface class; used to define content-type schema.

class IAgreementFileField(INamedBlobFileField):
    pass

class AgreementFile(NamedBlobFile):
    implements(IAgreementFileField)

class IProducent(model.Schema, IImageScaleTraversable):
    """
    E-Deposit Producent
    """
    pravni_forma = schema.TextLine(
        title = u"Právní forma",
        required = False,
    )

    domicile = schema.TextLine(
        title = u"Sídlo (celá adresa)",
        required = False, )

    ico = schema.ASCIILine (
        title = u"IČ",
        required = False )

    dic = schema.ASCIILine (
        title = u"DIČ",
        required = False )

    zastoupen = schema.TextLine (
        title = u"Statutární zástupce organizace",
        required = False )

    agreement = AgreementFile (
        title=_(u'Agreement'),
        description = _(u'Upload file with agreement between National Library and you.'),
        required = False,
    )        
    model.fieldset( 'agreement',
                    label=_(u"Agreement with National Library"),
                    fields = ['agreement',]
    )
    
class Producent(Container):
    # Add your class methods and properties here
    def hasAgreement(self):
        return bool(self.agreement)

    def ensureRolesConsistency(self):
        assigned_members = frozenset((self.getAssignedProducentAdministrators() or [])\
                                         + (self.getAssignedProducentEditors() or []))
        members = frozenset(self.getAssignedProducentMembers() or [])
        extra_assigned_members = assigned_members - members
        for userid in extra_assigned_members:
            api.user.grant_roles(username=userid, obj=self,roles = ('E-Deposit: Producent Member',))
        pass

    def createSummaryFolder(self):
        pass

    def getProducentMembers(self):
        def hasEmail(userid):
            return api.user.get(userid).getProperty('email')

        producentAdministrators = filter(hasEmail,self.getAssignedProducentAdministrators() or [])
        producentMembers = filter(hasEmail,self.getAssignedProducentMembers() or [])
        return frozenset(producentAdministrators + producentMembers)

    def notifyProducentAboutEPublicationsWithError(self):
        view = api.content.get_view(name='epublications-with-error-worklist',
                                    context = self,
                                    request = self.REQUEST)
        body = view()
        subject = "EDeposit: ePublikace s chybou"
        if view.numOfRows:
            def getOwners(brain):
                getter = getattr(brain,'get_local_roles')
                local_roles = (callable(getter) and getter()) or (not callable(getter) and getter)
                owners = [ii[0] for ii in local_roles if 'Owner' in ii[1]]
                return owners

            def hasEmail(userid):
                return api.user.get(userid).getProperty('email')
                
            producentAdministrators = filter(hasEmail,self.getAssignedProducentAdministrators() or [])
            producentMembers = filter(hasEmail,self.getAssignedProducentMembers() or [])
            
            def usersToNotify(brain):
                owners = filter(hasEmail,getOwners(brain))
                if owners:
                    return owners
                if producentAdministrators:
                    return producentAdministrators
                if producentMembers:
                    return producentMembers
                return []

            def iterateUsers(brains):
                for brain in brains:
                    users = usersToNotify(brain)
                    for user in users:
                        yield (user, brain)

            brainsByUser = defaultdict(list)
            for userid, brain in iterateUsers(view.brains):
                brainsByUser[userid].append(brain)

            for user, brains in brainsByUser.items():
                recipient = api.user.get(user).getProperty('email')
                print "... posilam email: ", subject,"->", recipient
                body = view.tmpl.substitute(csvData = view.getCSVData(brains))
                api.portal.send_email(recipient = recipient, subject=subject, body=body)
                api.portal.send_email(recipient = 'stavel.jan@gmail.com', subject=subject, body=body)

def getAssignedPersonFactory(roleName):
    def getAssignedPerson(self):
        local_roles = self.get_local_roles()
        pairs = filter(lambda pair: roleName in pair[1], local_roles)
        return pairs and [ pp[0] for pp in pairs ] or None

    return getAssignedPerson

Producent.getAssignedProducentAdministrators = getAssignedPersonFactory('E-Deposit: Producent Administrator')
Producent.getAssignedProducentEditors = getAssignedPersonFactory('E-Deposit: Producent Editor')
Producent.getAssignedProducentMembers = getAssignedPersonFactory('E-Deposit: Producent Member')


def getTermFromMember(member):
    return SimpleVocabulary.createTerm(member.id, member.id, "%s (%s)" % (member.getProperty('fullname'),member.id))

class SearchSimpleVocabulary(SimpleVocabulary):
    def search(self, query_string):
        return [v for v in self if query_string.lower() in v.title.lower()]
        
@grok.provider(IContextSourceBinder)
def allProducentAdministrators(context):
    members = api.user.get_users(groupname="Producent Administrators")
    return SearchSimpleVocabulary(map(getTermFromMember, members))
    
@grok.provider(IContextSourceBinder)
def allProducentEdidtors(context):
    members = api.user.get_users(groupname="Producent Editors")
    return SearchSimpleVocabulary(map(getTermFromMember, members))

@grok.provider(IContextSourceBinder)
def allProducentMembers(context):
    members = filter(lambda item: item is not None, map(api.user.get,context.getAssignedProducentMembers()))
    return SearchSimpleVocabulary(map(getTermFromMember, members))

@grok.provider(IContextSourceBinder)
def allProducentMembersWithoutCurrent(context):
    current_user = api.user.get_current()
    members =  filter(partial(is_not,None),
                      map(api.user.get,
                          filter(partial(ne, current_user.id),
                                 context.getAssignedProducentMembers())))

    return SearchSimpleVocabulary(map(getTermFromMember, members))
    
class IProducentUsersForm(form.Schema):
    form.widget(administrators=CheckBoxFieldWidget)    
    administrators = schema.Set (
        title = u"Správci",
        value_type = schema.Choice(source = allProducentMembers)
        )

    form.widget(editors=CheckBoxFieldWidget)    
    editors = schema.Set (
        title = u"Editoři",
        value_type = schema.Choice(source = allProducentMembers)
        )

class ProducentToProducentUsers(object):
    implements(IProducentUsersForm)
    adapts(IProducent)

    def __init__(self, context):
        self.context = context
        self.administrators = self.context.getAssignedProducentAdministrators()
        self.editors = self.context.getAssignedProducentEditors()
    

class ProducentUsersForm(form.SchemaForm):
    schema = IProducentUsersForm
    ignoreContext = False
    label = u"Vyberte pracovníky"

    @button.buttonAndHandler(u"Nastavit oprávnění",name="save")
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        localRoles = self.context.get_local_roles()
        oldAdministrators = map(lambda ii: ii[0],filter(lambda role: 'E-Deposit: Producent Administrator' in role[1],localRoles))
        oldEditors = map(lambda ii: ii[0],filter(lambda role: 'E-Deposit: Producent Editor' in role[1],localRoles))

        for userid in oldAdministrators:
            api.user.revoke_roles(obj=self.context, username=userid, roles=('E-Deposit: Producent Administrator',
                                                                            'Editor','Reader'))
            api.user.revoke_roles(obj=self.context['epublications'],
                                  username=userid,
                                  roles=( 'E-Deposit: Producent Administrator',))

        for userid in oldEditors:
            api.user.revoke_roles(obj=self.context, username=userid, roles=('E-Deposit: Producent Editor',
                                                                            'Editor','Reader'))
            api.user.revoke_roles(obj=self.context['epublications'],
                                  username=userid,
                                  roles=( 'E-Deposit: Producent Editor', 'Contributor'))

        for userid in data['administrators']:
            api.user.grant_roles(username=userid, obj=self.context,
                                 roles = ('E-Deposit: Producent Member',
                                          'E-Deposit: Producent Editor',
                                          'E-Deposit: Producent Administrator',
                                          'Editor', 'Reader'))
            api.user.grant_roles(username=userid, obj=self.context['epublications'],
                                 roles = ('E-Deposit: Producent Member',
                                          'E-Deposit: Producent Editor',
                                          'E-Deposit: Producent Administrator',
                                          'Contributor'))
        for userid in data['editors']:
            api.user.grant_roles(username=userid, obj=self.context,
                                 roles = ('E-Deposit: Producent Editor',
                                          'Editor', 'Reader'))
            api.user.grant_roles(username=userid, obj=self.context['epublications'],
                                 roles = ('E-Deposit: Producent Editor',
                                          'Contributor'))
        IStatusMessage(self.request).addStatusMessage(u"Role byly nastaveny.", "info")
        url = self.context.absolute_url()
        self.request.response.redirect(url)
        self.context.reindexObject()
    pass
    
from edeposit.user.browser import register

class IProducentMember(model.Schema):
    """ a few fields from IProducentAdministrator """
    fullname = schema.TextLine(
        title=u"Jméno a příjmení",
        description=_(u'help_full_name_creation',
                      default=u"Enter full name, e.g. John Smith."),
        required=True)

    email = schema.ASCIILine(
        title=_(u'label_email', default=u'E-mail'),
        description=u'',
        constraint = register.checkEmailAddress,
        required=True,
    )

    phone = schema.ASCIILine(
        title=_(u'label_phone', default=u'Telephone number'),
        description=_(u'help_phone',
                      default=u"Leave your phone number so we can reach you."),
        required=True,
        constraint = register.checkForRegularTextFactory(r'^[ 0-9\+]*$'),
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
        required=True,
        constraint = register.checkForRegularTextFactory(r'^[a-z0-9_\.A-Z]{5,32}$'),
    )
    
    password = schema.Password(
        title=_(u'label_password', default=u'Password'),
        description=_(u'help_password_creation',
                      default=u'Enter your new password.'),
        required=True,
    )
    
    password_ctl = schema.Password(
        title=_(u'label_confirm_password',
                default=u'Confirm password'),
        description=_(u'help_confirm_password',
                      default=u"Re-enter the password. "
                      "Make sure the passwords are identical."),
        required=True,
    )


class ProducentAddEditorForm(form.SchemaForm):
    schema = IProducentMember
    ignoreContext = True
    enableCSRFProtection = True
    enable_form_tabbing = False
    label = u"Nový editor"

    def extractData(self):
        def getErrorView(widget,error):
            view = getMultiAdapter( (error, 
                                     self.request, 
                                     widget, 
                                     widget.field, 
                                     widget.form, 
                                     self.context), 
                                    IErrorViewSnippet)
            view.update()
            widget.error = view
            return view

        reg_tool = api.portal.get_tool(name='portal_registration')
        widgets = self.widgets

        data,errors = super(ProducentAddEditorForm,self).extractData()

        username = data.get('username')
        if username and api.user.get(username = username):
            errors += (getErrorView(widgets.get('username'),
                                    Invalid(u"Uživatelské jméno je již použito. Vyplňte jiné.")),)
            pass
            
        pwd1 = data.get('password')
        pwd2 = data.get('password_ctl')
        if pwd1 and len(pwd1) < 5:
            errors += (getErrorView(widgets.get('password'), 
                                    Invalid(u"Heslo je krátké. Nejméně 5 znaků.")),)
        if pwd2 and len(pwd2) < 5:
            errors += (getErrorView(widgets.get('password_ctl'), 
                                    Invalid(u"Heslo je krátké. Nejméně 5 znaků.")),)
        if (pwd1 and pwd2) and (len(pwd1) >= 5 and len(pwd2) >= 5) and  (pwd1 != pwd2):
            errors += (getErrorView(widgets.get('password'),  Invalid(u"Hesla se neshodují.")),)
            errors += (getErrorView(widgets.get('password_ctl'),  Invalid(u"Hesla se neshodují.")),)

        email = data.get('email')
        if email and not reg_tool.isValidEmail(email):
            errors += (getErrorView(widgets.get('email'),  Invalid(u"Toto není platný email.")),)

        return data,errors

    def setMemberRoles(self, member):
        api.group.add_user(groupname="Producent Editors", username=member.id)
        api.group.add_user(groupname="Producent Contributors", username=member.id)
        api.user.grant_roles(username=member.id,  obj=self.context,
                             roles=('E-Deposit: Producent Member',
                                    'E-Deposit: Producent Editor',
                                    'Reader'))
        pass

    def setStatusMessage(self):
        IStatusMessage(self.request).addStatusMessage(u"Vytvořen nový editor.", "info")
        
    @button.buttonAndHandler(u"Vytvořit",name="save")
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        userFields = ('username','password','email')
        propertyFields = ('fullname','phone')
        kwargs = dict(zip(userFields, map(data.__getitem__, userFields)))
        properties = dict(zip(propertyFields, map(data.__getitem__, propertyFields)))
        member = api.user.create(properties = properties, **kwargs)

        self.setMemberRoles(member)
        self.setStatusMessage()

        url = self.context.absolute_url()
        self.request.response.redirect(url)
        self.context.reindexObject()
    pass
    
class ProducentAdministratorAddForm(ProducentAddEditorForm):
    label = u"Nový správce"
    
    def setMemberRoles(self, member):
        api.group.add_user(groupname="Producent Editors", username=member.id)
        api.group.add_user(groupname="Producent Administrators", username=member.id)
        api.group.add_user(groupname="Producent Contributors", username=member.id)

        api.user.grant_roles(username=member.id,  obj=self.context,
                             roles=('E-Deposit: Producent Member',
                                    'E-Deposit: Producent Administrator',
                                    'E-Deposit: Producent Editor',
                                    'Editor','Reader'))
        
    def setStatusMessage(self):
        IStatusMessage(self.request).addStatusMessage(u"Vytvořen nový správce.", "info")

class IProducentRemoveUsersForm(form.Schema):
    form.widget(users=CheckBoxFieldWidget)
    users = schema.Set (
        title = u"Členové ke zrušení",
        value_type = schema.Choice(source = allProducentMembersWithoutCurrent)
    )

class ProducentRemoveUsersForm(form.SchemaForm):
    schema = IProducentRemoveUsersForm
    ignoreContext = True
    enableCSRFProtection = True
    enable_form_tabbing = False
    label = u"Zrušit uživatele"

    @button.buttonAndHandler(u"Zrušit vybrané uživatele",name="remove")
    def handleRemove(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        users = frozenset([ii for ii in data['users']])
        for user in users:
            api.group.remove_user(groupname="Producent Editors", username=user)
            api.group.remove_user(groupname="Producent Administrators", username=user)
            # api.user.revoke_roles(username=user,  obj=self.context,
            #                       roles=('E-Deposit: Producent Member',
            #                              'E-Deposit: Producent Administrator',
            #                              'E-Deposit: Producent Editor',
            #                              'Editor','Reader'))
            # api.user.delete(user)

        mtool = api.portal.get_tool('portal_membership')
        mtool.deleteLocalRoles(self.context, users, recursive=True)
        IStatusMessage(self.request).addStatusMessage(u"Vybraní uživatelé byli vymazáni.", "info")

        url = self.context.absolute_url()
        self.request.response.redirect(url)
        self.context.reindexObject()

class EPublicationsWithErrorWorklist(BrowserView):
    """Export the worklist to CSV as a one-off
    """
    tmpl = Template(u"""Dobrý den, posíláme Vám přehled ohlášených ePublikací, co čekají na Vaši opravu.

$csvData

ePublikaci do linky můžete odeslat tak, že:
- vyměníte, nebo opět vložíte přiložený soubor

S pozdravem,
tým E-Deposit
Národní Knihovna České Republiky
""")

    filename = "originaly-co-cekaji-na-opravu"
    collection_name = ""
    separator = "\t"
    titles = [u"Název", 
              u"Název části",
              u"Linka v E-Deposit"]

    def getRowValues(self,obj):
        row =  [obj.getParentTitle or "", 
                obj.getNazevCasti or "",
                obj.getURL() or ""]
        return row

    def getCSVData(self, brains):
        def result(brain):
            return self.separator.join(self.getRowValues(brain))

        results = map(result, brains)
        header = self.separator.join(self.titles)
        csvData = "\n".join([header,] + results)
        return csvData

    def __call__(self):
        #self.request.response.setHeader("Content-type","text/plain")
        #self.request.response.setHeader("Content-disposition","attachment;filename=%s.txt" % self.filename)
        pcatalog = self.context.portal_catalog
        folder_path = '/'.join(self.context.epublications.getPhysicalPath())
        pathQuery = dict(query=folder_path, depth=2)
        self.brains = pcatalog(portal_type="edeposit.content.originalfile", 
                               path=pathQuery, 
                               review_state='declarationWithError')
        self.numOfRows = len(self.brains)
        csvData = self.getCSVData(self.brains)
        return EPublicationsWithErrorWorklist.tmpl.substitute(csvData = csvData)
