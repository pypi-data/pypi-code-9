# coding: utf-8
from jsl.fields import compound, primitive


class HyperSchemaMixin(object):
    def _extend_schema(self, schema, *args):
        schema = super(HyperSchemaMixin, self)._extend_schema(schema, *args)
        if self._kwargs.get('read_only'):
            schema['readOnly'] = True
        # TODO
        return schema


class ArrayField(HyperSchemaMixin, compound.ArrayField):
    pass


class DictField(HyperSchemaMixin, compound.DictField):
    pass


class OneOfField(HyperSchemaMixin, compound.OneOfField):
    pass


class AnyOfField(HyperSchemaMixin, compound.AnyOfField):
    pass


class AllOfField(HyperSchemaMixin, compound.AllOfField):
    pass


class StringField(HyperSchemaMixin, primitive.StringField):
    pass


class BooleanField(HyperSchemaMixin, primitive.BooleanField):
    pass


class EmailField(HyperSchemaMixin, primitive.EmailField):
    pass


class IPv4Field(HyperSchemaMixin, primitive.IPv4Field):
    pass


class DateTimeField(HyperSchemaMixin, primitive.DateTimeField):
    pass


class UriField(HyperSchemaMixin, primitive.UriField):
    pass


class NumberField(HyperSchemaMixin, primitive.NumberField):
    pass


class IntField(HyperSchemaMixin, primitive.IntField):
    pass


class NullField(HyperSchemaMixin, primitive.NullField):
    pass


print ArrayField()._extend_schema({})
