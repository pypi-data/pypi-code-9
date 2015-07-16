# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.interface import alsoProvides
from zope import schema
from zope.component import adapter
from plone.supermodel import model
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

_ = lambda x: x


class IHeaderAndFooter(model.Schema):

    custom_header = schema.Choice(
        title=_(u'Custom header'),
        required=False,
        vocabulary='localheaderandfooter.available_headers'
    )

    custom_footer = schema.Choice(
        title=_(u'Custom footer'),
        required=False,
        vocabulary='localheaderandfooter.available_footers'
    )

alsoProvides(IHeaderAndFooter, IFormFieldProvider)


@adapter(IDexterityContent)
@implementer(IHeaderAndFooter)
class HeaderAndFooter(object):

    def __init__(self, context):
        self.context = context

    @property
    def custom_header(self):
        return getattr(self.context, 'custom_header', None)

    @custom_header.setter
    def custom_header(self, value):
        setattr(self.context, 'custom_header', value)

    @property
    def custom_footer(self):
        return getattr(self.context, 'custom_footer', None)

    @custom_footer.setter
    def custom_footer(self, value):
        setattr(self.custom_footer, 'custom_footer', value)
