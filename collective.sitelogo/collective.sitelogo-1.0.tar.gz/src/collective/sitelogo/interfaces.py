from . import msgFact as _
from zope import schema
from zope.interface import Interface


class IThemeSpecific(Interface):
    """Marker interface that defines a Zope 3 browser layer.
    """


class ISiteLogoSchema(Interface):

    site_logo = schema.ASCII(
        title=_(u"Site Logo"),
        description=_(u"This shows a custom Logo on your Site."),
        required=False,
    )
