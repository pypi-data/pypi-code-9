
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


# Interface class; used to define content-type schema.

class IAgreementFile(model.Schema, IImageScaleTraversable):
    """
    E-Deposit - file with agreement for producent
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/agreement_file.xml to define the content type.

    agreement = NamedBlobFile(
        title=_(u'Agreement'),
        description = _(u'Upload file with agreement between National Library and you.'),
        required = False,
        )        

    model.primary('agreement')
    #model.load("models/agreement_file.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class AgreementFile(Container):

    # Add your class methods and properties here
    pass

# View class
# The view is configured in configure.zcml. Edit there to change
# its public name. Unless changed, the view will be available
# TTW at content/@@sampleview

class SampleView(BrowserView):
    """ sample view class """

    # Add view methods here
    pass
