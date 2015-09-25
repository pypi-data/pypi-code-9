from . import msgFact as _
from zope import schema
from zope.interface import Interface


class IThemeSpecific(Interface):
    """Marker interface that defines a Zope 3 browser layer.
    """


class ISiteLogoSchema(Interface):

    site_logo = schema.ASCII(
        title=_('label_site_logo', default=u"Site Logo"),
        description=_(
            'help_site_logo',
            default=u"This shows a custom Logo on your Site."
        ),
        required=False,
    )
