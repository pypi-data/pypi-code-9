# -*- coding: utf-8 -*-
from five import grok
import zope
import z3c.form
from z3c.form import group, field, button
from zope import schema
from zope.interface import invariant, Invalid, implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.lifecycleevent import modified
from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder, UUIDSourceBinder
from plone.formwidget.autocomplete import AutocompleteFieldWidget, AutocompleteMultiFieldWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory, IValidator, IErrorViewSnippet, INPUT_MODE
import pickle
import os.path
from functools import partial
from Products.Five.browser.metaconfigure import ViewMixinForTemplates
from Products.Five.browser import BrowserView

# 608748854 pan Rysavy, zamecnictvi, Zlin

from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds

from edeposit.content.library import ILibrary
from edeposit.content import MessageFactory as _

from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.supermodel import model
from plone.dexterity.utils import getAdditionalSchemata
from Acquisition import aq_inner, aq_base

from zope.component import adapts, createObject
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import Invalid, Interface
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory
from plone.dexterity.interfaces import IDexterityFTI
from collections import namedtuple
from plone import api
from zope.event import notify
from plone.dexterity.events import AddBegunEvent
from plone.dexterity.events import AddCancelledEvent
from plone.app.discussion.interfaces import IConversation
import operator
import z3c.form.browser.radio

import edeposit.amqp.aleph

from plone.z3cform.layout import wrap_form, FormWrapper

from edeposit.content.epublicationfolder import (
    IePublicationFolder,
)

from edeposit.content.utils import loadFromAlephByISBN
from edeposit.content.utils import is_valid_isbn
from edeposit.content.utils import getISBNCount
import z3c.form.browser
from z3c.formwidget.query.interfaces import IQuerySource
from functools import partial
from plone.memoize.view import memoize, memoize_contextless

from plone.api.user import get_users

class CataloguingMembers(object):
    implements(IContextSourceBinder)

    def __init__(self,groupName):
        self.groupName = groupName
        self.vocabulary = None

    def __contains__ (self, query):
        if not self.vocabulary:
            self.vocabulary = self.getVocabulary()

        return query in self.vocabulary

    def getVocabulary(self):
        members = get_users(groupname=self.groupName)
        pairs = [ dict(id=mm.id, fullname=mm.getProperty('fullname')) for mm in members ]
        createTerm = SimpleVocabulary.createTerm
        terms = [createTerm(mm['id'], mm['id'], (u"%s (%s)" % (mm['fullname'],mm['id'])).encode('utf-8')) 
                 for mm in pairs ]
        vocabulary = SimpleVocabulary(terms)

        def search(self,query):
            return [v for v in self if query.lower() in v.value.lower()]

        vocabulary.search = partial(search,vocabulary)
        return vocabulary

    def __call__ (self, context):
        self.vocabulary = self.getVocabulary()
        return self.vocabulary

class ISubjectCataloguingGroups(form.Schema):
    form.widget(cataloguers = z3c.form.browser.checkbox.CheckBoxFieldWidget)
    cataloguers = schema.Set (
        title = u"Katalogizátoři",
        value_type = schema.Choice(source = CataloguingMembers('Subject Cataloguing Members'))
    )
    form.widget(reviewers = z3c.form.browser.checkbox.CheckBoxFieldWidget)
    reviewers = schema.Set (
        title = u"Revizoři",
        value_type = schema.Choice(source = CataloguingMembers('Subject Cataloguing Members'))
    )

class SubjectCataloguingGroupsAdministrationForm(form.SchemaForm):
    schema = ISubjectCataloguingGroups
    ignoreContext = True
    label = u"Správa členů věcného popisu"

    def actualCataloguers(self):
        ids =  lambda groupname: set([mm.id for mm in get_users(groupname=groupname)])
        return ids('Subject Cataloguers') & ids('Subject Cataloguing Members')

    def actualReviewers(self):
        ids =  lambda groupname: set([mm.id for mm in get_users(groupname=groupname)])
        return ids('Subject Cataloguing Reviewers')  & ids('Subject Cataloguing Members')

    def updateWidgets(self):
        self.fields['cataloguers'].field.default = self.actualCataloguers()
        self.fields['reviewers'].field.default = self.actualReviewers()
        super(SubjectCataloguingGroupsAdministrationForm,self).updateWidgets()

    @button.buttonAndHandler(u"Nastavit skupiny",name="save")
    def handleSubmit(self, action):
        data, errors = self.extractData()
        if errors:
            return
        
        ids = lambda groupname: frozenset([mm.id for mm in get_users(groupname=groupname)])

        toBeRemoved = ids('Subject Cataloguers') & ids('Subject Cataloguing Members')
        for username in toBeRemoved:
            api.group.remove_user(groupname='Subject Cataloguers', username=username)

        for username in data['cataloguers']:
            api.group.add_user(groupname='Subject Cataloguers', username=username)

        toBeRemoved = ids('Subject Cataloguing Reviewers') & ids('Subject Cataloguing Members')
        for username in toBeRemoved:
            api.group.remove_user(groupname='Subject Cataloguing Reviewers', username=username)

        for username in data['reviewers']:
            api.group.add_user(groupname='Subject Cataloguing Reviewers', username=username)


class IDescriptiveCataloguingGroups(form.Schema):
    form.widget(cataloguers = z3c.form.browser.checkbox.CheckBoxFieldWidget)
    cataloguers = schema.Set(
        title = u"Katalogizátoři",
        value_type = schema.Choice(source = CataloguingMembers('Descriptive Cataloguing Members'))
    )
    form.widget(reviewers = z3c.form.browser.checkbox.CheckBoxFieldWidget)
    reviewers = schema.Set(
        title = u"Revizoři",
        value_type = schema.Choice(source = CataloguingMembers('Descriptive Cataloguing Members'))
    )

class DescriptiveCataloguingGroupsAdministrationForm(form.SchemaForm):
    schema = IDescriptiveCataloguingGroups
    ignoreContext = True
    label = u"Správa členů jmenného popisu"

    def actualCataloguers(self):
        ids = lambda groupname: set([mm.id for mm in get_users(groupname=groupname)])
        return ids('Descriptive Cataloguers') & ids('Descriptive Cataloguing Members')

    def actualReviewers(self):
        ids = lambda groupname: set([mm.id for mm in get_users(groupname=groupname)])
        return ids('Descriptive Cataloguing Reviewers')  & ids('Descriptive Cataloguing Members')

    def updateWidgets(self):
        self.fields['cataloguers'].field.default = self.actualCataloguers()
        self.fields['reviewers'].field.default = self.actualReviewers()
        super(DescriptiveCataloguingGroupsAdministrationForm,self).updateWidgets()

    @button.buttonAndHandler(u"Nastavit skupiny",name="save")
    def handleSubmit(self, action):
        data, errors = self.extractData()
        if errors:
            return
        
        ids = lambda groupname: frozenset([mm.id for mm in get_users(groupname=groupname)])

        toBeRemoved = ids('Descriptive Cataloguers') & ids('Descriptive Cataloguing Members')
        for username in toBeRemoved:
            api.group.remove_user(groupname='Descriptive Cataloguers', username=username)

        for username in data['cataloguers']:
            api.group.add_user(groupname='Descriptive Cataloguers', username=username)

        toBeRemoved = ids('Descriptive Cataloguing Reviewers') & ids('Descriptive Cataloguing Members')
        for username in toBeRemoved:
            api.group.remove_user(groupname='Descriptive Cataloguing Reviewers', username=username)

        for username in data['reviewers']:
            api.group.add_user(groupname='Descriptive Cataloguing Reviewers', username=username)


