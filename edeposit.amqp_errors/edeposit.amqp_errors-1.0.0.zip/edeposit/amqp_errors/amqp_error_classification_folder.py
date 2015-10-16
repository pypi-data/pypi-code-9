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

from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

from edeposit.amqp_errors import MessageFactory as _
from plone.z3cform.layout import FormWrapper
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from plone.dexterity.utils import createContentInContainer

class IAMQPErrorClassificationFolder(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/amqp_error_classification_folder.xml to define the content type.

    form.model("models/amqp_error_classification_folder.xml")

from operator import __eq__, itemgetter

class AMQPErrorClassificationFolder(Container):
    grok.implements(IAMQPErrorClassificationFolder)

    def getTrainData(self):
        items = filter(lambda pp: pp[1].portal_type == 'edeposit.amqp_errors.amqperrorclassification', self.items())
        trainData = map(lambda item: (item.errorText, item.errorType), map(itemgetter(1), items))
        return trainData

    def classifierFactory(self, trainData):
        return NaiveBayesClassifier(trainData)

    def updateClassificator(self):
        self.classificator = self.classifierFactory(self.getTrainData())

    def classifyError(self,errorText):
        if not getattr(self,'classifier',None):
            self.classifier = self.classifierFactory(self.getTrainData())

        prob_cl = self.classifier.prob_classify(errorText)
        result = prob_cl.max()
        return (result, prob_cl.prob(result))


    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# amqp_error_classification_folder_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.


class IUploadForm(form.Schema):
    csv_file = NamedFile(title=u"CSV soubor s daty")


class UploadForm(form.SchemaForm):
    grok.context(IAMQPErrorClassificationFolder)
    schema = IUploadForm
    ignoreContext = True
    description = u"- ma hlavicku, ma dva sloupecky: text, klasifikaci. oddelene znakem: |"

    @button.buttonAndHandler(u"Upload CSV", name="upload-csv")
    def uploadCSV(self,action):
        import csv
        import StringIO
        
        data,errors = self.extractData()
        if errors:
            self.status = u"Please correct errors"
            return

        csvdata = StringIO.StringIO(data['csv_file'].data)
        reader = csv.reader(csvdata,delimiter="|")
        for text,status in reader:
            createContentInContainer(self.context, 'edeposit.amqp_errors.amqperrorclassification', 
                                     errorText=text,
                                     errorType=status)

class UploadFormWrapper(FormWrapper):
    index = ViewPageTemplateFile("formwrapper.pt")

class TrainClassificatorView(grok.View):
    """ sample view class """

    grok.context(IAMQPErrorClassificationFolder)
    grok.require('zope2.View')
    grok.name('train-classificator')

    def __call__(self):
        context = self.context.aq_inner
        form = UploadForm(context, self.request)
        view = UploadFormWrapper(context, self.request)
        view = view.__of__(context)
        view.form_instance = form
        self.form_wrapper = view
        return super(TrainClassificatorView,self).__call__()
