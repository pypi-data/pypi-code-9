from plone.app.textfield import RichText
from plone.dexterity.content import Item
from plone.directives.form import Schema
from plone.namedfile.field import NamedFile
from plone.namedfile.field import NamedImage
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary


COLORS = SimpleVocabulary.fromValues([u'Red', 'Blue', 'Green'])


class IDXItemSchema(Schema):

    bool_field = schema.Bool(title=u'Bool Field', default=False)
    choice_field = schema.Choice(title=u'Choice Field', vocabulary=COLORS)
    date_field = schema.Date(title=u'Date Field')
    datetime_field = schema.Datetime(title=u'Datetime Field')
    decimal_field = schema.Decimal(title=u'Float Field')
    dottedname_field = schema.URI(title=u'DottedName Field')
    file_field = NamedFile(title=u'File Field')
    float_field = schema.Float(title=u'Float Field')
    image_field = NamedImage(title=u'Image Field')
    list_field = schema.List(title=u'List Field')
    richtext_field = RichText(title=u'Rich Text Field')
    text_field = schema.Text(title=u'Text Field')
    time_field = schema.Time(title=u'Time Field')
    timedelta_field = schema.Timedelta(title=u'Timedelta Field')
    uri_field = schema.URI(title=u'URI Field')


class DXItem(Item):
    pass
