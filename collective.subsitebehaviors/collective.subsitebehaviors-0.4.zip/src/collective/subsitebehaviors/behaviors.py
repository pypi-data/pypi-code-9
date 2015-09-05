from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model


from . import _

class ISubSite(model.Schema):
   """Behavior interface to add a customer logo etc.
   """

   model.fieldset('appearance', label=_("fieldset_appearance", u"Appearance"), fields=['logoImage'])

   logoImage = NamedBlobImage(
      title=_("field_customlogo", u"Custom logo"),
      description=_("field_customlogo_description", u"Custom logo to be used"),
      required=False
   )

alsoProvides(ISubSite, IFormFieldProvider)
