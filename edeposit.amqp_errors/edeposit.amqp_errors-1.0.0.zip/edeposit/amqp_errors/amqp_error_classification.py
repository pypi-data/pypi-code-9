# -*- coding: utf-8 -*-
from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


from edeposit.amqp_errors import MessageFactory as _


errorTypeChoices = [
    ['middleware-problem',   u"Problém v systému"],
    ['file-problem', u"Problém s dokumentem"],
    ['only-czech-isbn-accepted', u"Přijímáme pouze česká ISBN"],
    ['document-was-deleted', u"Záznam v Alephu byl smazán"],
    ['zpracovatel-is-required', u"Pole zpracovatel je povinné"],
    ['isbn-already-exists', u"ISBN již bylo použito"],
    ['wrong-isbn', u"Chyba v ISBN"],
    ['unknown', u"Neznámá chyba"],
    ['datum-vydani-is-required', u"Pole datum vydaní je povinné"],
]

@grok.provider(IContextSourceBinder)
def availableErrorTypes(context):
    def getTerm(item):
        title = item[1].encode('utf-8')
        return SimpleVocabulary.createTerm(item[0], item[0], title)

    return SimpleVocabulary(map(getTerm, errorTypeChoices))

# Interface class; used to define content-type schema.

class IAMQPErrorClassification(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """
    errorText = schema.Text (
        title=u"Text chyby",
        required=True,
    )
    
    errorType = schema.Choice(
        title = u"Typ chyby",
        required = True,
        source = availableErrorTypes
    )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class AMQPErrorClassification(Container):
    grok.implements(IAMQPErrorClassification)
    # Add your class methods and properties here
    

# View class
# The view will automatically use a similarly named template in
# amqp_error_classification_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IAMQPErrorClassification)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
