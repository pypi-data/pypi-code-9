#
# Copyright (c) 2015, Prometheus Research, LLC
#


import re

from copy import deepcopy

import colander

from six import iteritems, string_types, integer_types

from .common import ValidationError, sub_schema, AnyType, LanguageTag, \
    validate_instrument_version
from .instrument import InstrumentReference, IdentifierString, \
    get_full_type_definition


__all__ = (
    'METADATA_SCOPE_ASSESSMENT',
    'METADATA_SCOPE_VALUE',
    'METADATA_STANDARD_PROPERTIES',

    'MetadataCollection',
    'ValueCollection',
    'Assessment',
)


RE_PRODUCT_TOKEN = re.compile(r'^(.+)/(.+)$')
RE_DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
RE_TIME = re.compile(r'^\d{2}:\d{2}:\d{2}$')
RE_DATETIME = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$')

METADATA_SCOPE_ASSESSMENT = 'assessment'
METADATA_SCOPE_VALUE = 'value'

METADATA_STANDARD_PROPERTIES = {
    METADATA_SCOPE_ASSESSMENT: {
        'language': LanguageTag(),
        'application': colander.SchemaNode(
            colander.String(),
            validator=colander.Regex(RE_PRODUCT_TOKEN),
        ),
        'dateCompleted': colander.SchemaNode(
            colander.DateTime(),
        ),
        'timeTaken': colander.SchemaNode(
            colander.Integer(),
        ),
    },

    METADATA_SCOPE_VALUE: {
        'timeTaken': colander.SchemaNode(
            colander.Integer(),
        ),
    },
}


# pylint: disable=abstract-method


class MetadataCollection(colander.SchemaNode):
    def __init__(self, scope, *args, **kwargs):
        self.scope = scope
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(MetadataCollection, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if len(cstruct) == 0:
            raise ValidationError(
                node,
                'At least one propety must be defined',
            )

        standards = METADATA_STANDARD_PROPERTIES.get(self.scope, {})

        for prop, value in iteritems(cstruct):
            if prop in standards:
                sub_schema(standards[prop], node, value)


class Value(colander.SchemaNode):
    value = colander.SchemaNode(
        AnyType(),
    )
    explanation = colander.SchemaNode(
        colander.String(),
        missing=colander.drop,
    )
    annotation = colander.SchemaNode(
        colander.String(),
        missing=colander.drop,
    )
    meta = MetadataCollection(
        METADATA_SCOPE_VALUE,
        missing=colander.drop,
    )

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Value, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if isinstance(cstruct['value'], list):
            for subtype in (
                    colander.SchemaNode(colander.String()),
                    ValueCollection):
                for value in cstruct['value']:
                    try:
                        sub_schema(subtype, node, value)
                    except ValidationError:
                        break
                else:
                    return

            raise ValidationError(
                node,
                'Lists must be consist only of Strings or ValueCollections',
            )

        elif isinstance(cstruct['value'], dict):
            sub_schema(ValueCollectionMapping, node, cstruct['value'])


class ValueCollection(colander.SchemaNode):
    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(ValueCollection, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if len(cstruct) == 0:
            raise ValidationError(
                node,
                'At least one Value must be defined',
            )

        for field_id, value in iteritems(cstruct):
            sub_schema(IdentifierString, node, field_id)
            sub_schema(Value, node, value)


class ValueCollectionMapping(colander.SchemaNode):
    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(ValueCollectionMapping, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if len(cstruct) == 0:
            raise ValidationError(
                node,
                'At least one Row must be defined',
            )

        for field_id, values in iteritems(cstruct):
            sub_schema(IdentifierString, node, field_id)
            sub_schema(ValueCollection, node, values)


VALUE_TYPE_CHECKS = {
    'integer': lambda val: isinstance(val, integer_types),
    'float': lambda val: isinstance(val, (float,) + integer_types),
    'text': lambda val: isinstance(val, string_types),
    'enumeration': lambda val: isinstance(val, string_types),
    'boolean': lambda val: isinstance(val, bool),
    'date': lambda val: isinstance(val, string_types) and RE_DATE.match(val),
    'time': lambda val: isinstance(val, string_types) and RE_TIME.match(val),
    'dateTime':
    lambda val: isinstance(val, string_types) and RE_DATETIME.match(val),
    'enumerationSet': lambda val: isinstance(val, list),
    'recordList': lambda val: isinstance(val, list),
    'matrix': lambda val: isinstance(val, dict),
}


class Assessment(colander.SchemaNode):
    instrument = InstrumentReference()
    meta = MetadataCollection(
        METADATA_SCOPE_ASSESSMENT,
        missing=colander.drop,
    )
    values = ValueCollection()

    def __init__(self, instrument=None, *args, **kwargs):
        self.instrument = instrument
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Assessment, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if not self.instrument:
            return

        validate_instrument_version(
            self.instrument,
            cstruct,
            node.get('instrument'),
        )

        self.check_has_all_fields(
            node.get('values'),
            cstruct['values'],
            self.instrument['record'],
        )

    def check_has_all_fields(self, node, values, fields):
        values = deepcopy(values)
        if not isinstance(values, dict):
            raise ValidationError(
                node,
                'Value expected to contain a mapping.'
            )

        for field in fields:
            value = values.pop(field['id'], None)
            if value is None:
                raise ValidationError(
                    node,
                    'No value exists for field ID "%s"' % field['id'],
                )

            if value['value'] is None and field.get('required', False):
                raise ValidationError(
                    node,
                    'No value present for required field ID "%s"' % (
                        field['id'],
                    ),
                )

            full_type_def = get_full_type_definition(
                self.instrument,
                field['type'],
            )

            self._check_value_type(node, value['value'], field, full_type_def)

            self._check_metafields(node, value, field)

            self._check_complex_subfields(node, full_type_def, value)

        if len(values) > 0:
            raise ValidationError(
                node,
                'Unknown field IDs found: %s' % ', '.join(list(values.keys())),
            )

    def _check_value_type(self, node, value, field, type_def):
        if value is None:
            return

        wrong_type_error = ValidationError(
            node,
            'Value for "%s" is not of the correct type' % (
                field['id'],
            ),
        )

        bad_choice_error = ValidationError(
            node,
            'Value for "%s" is not an accepted enumeration' % (
                field['id'],
            ),
        )

        # Basic checks
        if not VALUE_TYPE_CHECKS[type_def['base']](value):
            raise wrong_type_error

        # Deeper checks
        if type_def['base'] == 'enumerationSet':
            choices = list(type_def['enumerations'].keys())
            for subval in value:
                if not isinstance(subval, string_types):
                    raise wrong_type_error
                if subval not in choices:
                    raise bad_choice_error
        if type_def['base'] == 'enumeration':
            choices = list(type_def['enumerations'].keys())
            if value not in choices:
                raise bad_choice_error

    def _check_metafields(self, node, value, field):
        explanation = field.get('explanation', 'none')
        if 'explanation' in value \
                and value['explanation'] is not None \
                and explanation == 'none':
            raise ValidationError(
                node,
                'Explanation present where not allowed in field ID "%s"' % (
                    field['id'],
                ),
            )
        elif 'explanation' not in value and explanation == 'required':
            raise ValidationError(
                node,
                'Explanation missing for field ID "%s"' % (
                    field['id'],
                ),
            )

        annotation = field.get('annotation', 'none')
        if 'annotation' in value and value['annotation'] is not None:
            if annotation == 'none':
                raise ValidationError(
                    node,
                    'Annotation present where not allowed',
                )

            elif value['value'] is not None:
                raise ValidationError(
                    node,
                    'Annotation provided for non-empty value',
                )
        elif 'annotation' not in value \
                and annotation == 'required' \
                and value['value'] is None:
            raise ValidationError(
                node,
                'Annotation missing for field ID "%s"' % (
                    field['id'],
                ),
            )

    def _check_complex_subfields(self, node, full_type_def, value):
        if value['value'] is None:
            return

        if 'record' in full_type_def:
            for rec in value['value']:
                self.check_has_all_fields(
                    node,
                    rec,
                    full_type_def['record'],
                )

        elif 'rows' in full_type_def:
            for row in full_type_def['rows']:
                row_value = value['value'].pop(row['id'], None)
                if row_value is None:
                    raise ValidationError(
                        node,
                        'Missing values for row ID "%s"' % row['id'],
                    )

                self.check_has_all_fields(
                    node,
                    row_value,
                    full_type_def['columns'],
                )

            if len(value['value']) > 0:
                raise ValidationError(
                    node,
                    'Unknown row IDs found: %s' % (
                        ', '.join(list(value['value'].keys())),
                    ),
                )

