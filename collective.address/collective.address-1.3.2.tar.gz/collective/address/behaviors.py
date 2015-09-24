from Products.CMFPlone.utils import safe_unicode
from collective.address import messageFactory as _
from collective.address.vocabulary import get_pycountry_name
from plone.app.content.interfaces import INameFromTitle
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.indexer import indexer
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.component import adapter
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import implementer


class IAddressable(Interface):
    """Abstract marker interface.
    """


class IAddress(model.Schema, IAddressable):
    """Address schema.
    """
    street = schema.TextLine(
        title=_(u'label_street', default=u'Street'),
        description=_(u'help_street', default=u''),
        required=False
    )
    zip_code = schema.TextLine(
        title=_(u'label_zip_code', default=u'Zip Code'),
        description=_(u'help_zip_code', default=u''),
        required=False
    )
    city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        description=_(u'help_city', default=u''),
        required=False
    )
    country = schema.Choice(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country',
                      default=u'Select the country from the list.'),
        required=False,
        vocabulary='collective.address.CountryVocabulary'
    )


class IContact(model.Schema, IAddressable):
    """Contact schema.
    """
    email = schema.TextLine(
        title=_(u'label_email', default=u'Email'),
        description=_(u'help_email', default=u''),
        required=False
    )
    website = schema.TextLine(
        title=_(u'label_website', default=u'Website'),
        description=_(u'help_website', default=u''),
        required=False
    )
    phone = schema.TextLine(
        title=_(u'label_phone', default=u'Phone'),
        description=_(u'help_phone', default=u''),
        required=False
    )
    mobile = schema.TextLine(
        title=_(u'label_mobile', default=u'Mobile'),
        description=_(u'help_mobile', default=u''),
        required=False
    )
    fax = schema.TextLine(
        title=_(u'label_fax', default=u'Fax'),
        description=_(u'help_fax', default=u''),
        required=False
    )


class IPerson(model.Schema, IAddressable):
    """Person schema.
    """
    first_name = schema.TextLine(
        title=_(u'label_first_name', default=u'First Name'),
        description=_(u'help_first_name', default=u''),
        required=False
    )
    last_name = schema.TextLine(
        title=_(u'label_last_name', default=u'Last Name'),
        description=_(u'help_last_name', default=u''),
        required=True
    )
    academic_title = schema.TextLine(
        title=_(u'label_academic_titel', default=u'Academic title'),
        description=_(u'help_academic_title', default=u''),
        required=False
    )

    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=False,
        missing_value=u''
    )
    description = schema.Text(
        title=_PMF(u'label_description', default=u'Summary'),
        description=_PMF(
            u'help_description',
            default=u'Used in item listings and search results.'
        ),
        required=False,
        missing_value=u''
    )
    form.omitted('title', 'description')
    form.no_omit(IEditForm, 'description')
    form.no_omit(IAddForm, 'description')


# Mark these interfaces as form field providers
alsoProvides(IAddress, IFormFieldProvider)
alsoProvides(IContact, IFormFieldProvider)
alsoProvides(IPerson, IFormFieldProvider)


@implementer(INameFromTitle)
@adapter(IPerson)
class NameFromPerson(object):

    def __new__(cls, context):
        title = u'{0}{1}{2}'.format(
            context.last_name,
            ', ' if context.first_name else '',
            context.first_name
        )
        instance = super(NameFromPerson, cls).__new__(cls)
        instance.title = title
        context.title = title
        return instance

    def __init__(self, context):
        pass


def _concat_and_utf8(*args):
    """Concats args with spaces between and returns utf-8 string, it does not
    matter if input was unicode or str.
    Taken from ``plone.app.contenttypes.indexers``
    """
    result = ''
    for value in args:
        if isinstance(value, unicode):
            value = value.encode('utf-8', 'replace')
        if value:
            result = ' '.join((result, value))
    return result


# Text indexing
def searchable_text(obj):
    items = []

    acc = IAddress(obj, None)
    if acc:
        items += [
            safe_unicode(acc.street) or '',
            safe_unicode(acc.zip_code) or '',
            safe_unicode(acc.city) or '',
            safe_unicode(get_pycountry_name(acc.country)) if acc.country else ''  # noqa
        ]

    acc = IContact(obj, None)
    if acc:
        items += [
            safe_unicode(acc.email) or '',
            safe_unicode(acc.website) or '',
            safe_unicode(acc.phone) or '',
            safe_unicode(acc.mobile) or '',
            safe_unicode(acc.fax) or '',
        ]

    acc = IPerson(obj, None)
    if acc:
        items += [
            safe_unicode(acc.first_name) or '',
            safe_unicode(acc.last_name) or ''
        ]

    ret = _concat_and_utf8(*items)
    return ret


@indexer(IAddressable)
def searchable_text_indexer(obj):
    return searchable_text(obj)
