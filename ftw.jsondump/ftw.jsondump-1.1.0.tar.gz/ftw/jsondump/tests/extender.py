from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from plone.app.blob.field import FileField as FileBlobField
from plone.app.blob.field import ImageField as ImageBlobField
from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import ComputedField
from Products.Archetypes.atapi import FileField
from Products.Archetypes.atapi import FixedPointField
from Products.Archetypes.atapi import FloatField
from Products.Archetypes.atapi import ImageField
from Products.Archetypes.atapi import IntegerField
from Products.Archetypes.atapi import ReferenceField
from Products.ATContentTypes.content.document import IATDocument
from zope.component import adapts
from zope.interface import implements


class DemoIntegerField(ExtensionField, IntegerField):
    """Demo integer field"""


class DemoFloatField(ExtensionField, FloatField):
    """Demo float field"""


class DemoFixedPointField(ExtensionField, FixedPointField):
    """Demo fixed point field"""


class DemoComputedField(ExtensionField, ComputedField):
    """Demo computed field"""


class DemoBoolField(ExtensionField, BooleanField):
    """Demo boolean field"""


class DemoFileField(ExtensionField, FileField):
    """Demo file field"""


class DemoImageField(ExtensionField, ImageField):
    """Demo image field"""


class DemoFileBlobField(ExtensionField, FileBlobField):
    """Demo file blob field"""


class DemoImageBlobField(ExtensionField, ImageBlobField):
    """Demo image field"""


class DemoSingleRefField(ExtensionField, ReferenceField):
    """Demo single reference field"""


class DemoIntegerFieldExtender(object):

    adapts(IATDocument)
    implements(IOrderableSchemaExtender)

    fields = [
        DemoIntegerField('demo_interger_field'),
        DemoFloatField('demo_float_field'),
        DemoFixedPointField('demo_fixedpoint_field'),
        DemoBoolField('demo_bool_field'),
        DemoImageField('demo_image_field'),
        DemoFileField('demo_file_field'),
        DemoImageBlobField('demo_image_blob_field'),
        DemoFileBlobField('demo_file_blob_field'),
        DemoSingleRefField('demo_single_ref_field',
                           multiValued=False,
                           relationship="demo"),
        DemoComputedField('demo_computed_field',
                          expression='"Computed value"')]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, original):
        return original
