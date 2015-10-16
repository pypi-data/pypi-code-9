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

from plone.supermodel import model
from Products.Five import BrowserView

from edeposit.user import MessageFactory as _
from edeposit.user.producentuser import IProducentUser
from edeposit.user.producenteditorfolder import IProducentEditorFolder

from five import grok
from plone import api

from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from zope.interface import Invalid, Interface
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory

# Interface class; used to define content-type schema.

class IProducentEditor(IProducentUser):
    """
    E-Deposit Producent Editor
    """

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ProducentEditor(Container):

    # Add your class methods and properties here
    pass


# View class
# The view is configured in configure.zcml. Edit there to change
# its public name. Unless changed, the view will be available
# TTW at content/@@sampleview

class SampleView(BrowserView):
    """ sample view class """

    # Add view methods here

class ProducentEditorAddForm(DefaultAddForm):
    portal_type="edeposit.user.producenteditor"
    grok.context(IProducentEditorFolder)

    def add(self,object):
        if api.user.get(username=object.username):
            raise ActionExecutionError(Invalid(u"Uživatelské jméno již existuje. Na záložce Přihlášení použijte jiné."))
        if object.password != object.password_ctl:
            raise ActionExecutionError(Invalid(u"Hesla se neshodují. Na záložce Přihlášení zadejte hesla znovu."))
        return super(ProducentEditorAddForm,self).add(object)

class ProducentEditorAddView(DefaultAddView):
    form = ProducentEditorAddForm
    pass
