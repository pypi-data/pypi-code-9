#
# Copyright (c) 2015, Prometheus Research, LLC
#


import colander

from six import PY3

from .common import ValidationError, sub_schema, Options, \
    validate_instrument_version
from .instrument import InstrumentReference, IdentifierString, Description, \
    TYPES_SIMPLE

CAN_CHECK_HTSQL = False
if not PY3:
    try:
        from htsql import HTSQL
        from htsql.core.error import Error as HtsqlError
        from htsql.core.syn.parse import parse as parse_htsql
    except ImportError:  # pragma: no cover
        pass
    else:
        CAN_CHECK_HTSQL = True


__all__ = (
    'METHODS_ALL',

    'CalculationResultType',
    'CalculationMethod',
    'Expression',
    'PythonOptions',
    'HtsqlOptions',
    'Calculation',
    'CalculationList',
    'CalculationSet',
)


METHODS_ALL = (
    'python',
    'htsql',
)


_HTSQL = None


def get_htsql():
    global _HTSQL  # pylint: disable=global-statement
    if not _HTSQL and CAN_CHECK_HTSQL:
        _HTSQL = HTSQL({'engine': 'sqlite', 'database': ':memory:'})
    return _HTSQL


# pylint: disable=abstract-method


class CalculationResultType(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(TYPES_SIMPLE)


class CalculationMethod(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(METHODS_ALL)


class Expression(colander.SchemaNode):
    schema_type = colander.String


class PythonOptions(colander.SchemaNode):
    expression = Expression(missing=colander.drop)
    callable = Expression(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(PythonOptions, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if ('expression' in cstruct) == ('callable' in cstruct):
            raise ValidationError(
                node,
                'Exactly one option of "expression" or "callable" must be'
                ' specified',
            )

        expr = cstruct.get('expression', None)
        if expr and not PY3:
            try:
                compile(expr, '<string>', 'eval')
            except SyntaxError as exc:
                raise ValidationError(
                    node.get('expression'),
                    'The Python expression "%s" is invalid: %s' % (
                        expr,
                        exc,
                    ),
                )


class HtsqlOptions(colander.SchemaNode):
    expression = Expression()

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(HtsqlOptions, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        expr = cstruct.get('expression', None)
        if expr:
            htsql = get_htsql()
            if htsql:
                try:
                    with htsql:
                        parse_htsql(expr)
                except HtsqlError as exc:
                    raise ValidationError(
                        node.get('expression'),
                        'The HTSQL expression "%s" is invalid: %s' % (
                            expr,
                            exc,
                        ),
                    )


METHOD_OPTION_VALIDATORS = {
    'python': PythonOptions(),
    'htsql': HtsqlOptions(),
}


class Calculation(colander.SchemaNode):
    id = IdentifierString()  # pylint: disable=invalid-name
    description = Description()
    type = CalculationResultType()
    method = CalculationMethod()
    options = Options(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Calculation, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        method = cstruct.get('method', None)
        validator = METHOD_OPTION_VALIDATORS.get(method, None)
        options = cstruct.get('options', None)
        if validator:
            sub_schema(
                validator,
                node.get('options'),
                options,
            )
        elif options is not None:
            raise ValidationError(
                node.get('options'),
                'The "%s" method does not accept options' % method,
            )


class CalculationList(colander.SequenceSchema):
    calculation = Calculation()

    def validator(self, node, cstruct):
        if len(cstruct) < 1:
            raise ValidationError(
                node,
                'Shorter than minimum length 1',
            )

        ids = [calculation['id'] for calculation in cstruct]
        if len(ids) != len(set(ids)):
            raise ValidationError(
                node,
                'Calculation IDs must be unique',
            )


class CalculationSet(colander.SchemaNode):
    instrument = InstrumentReference()
    calculations = CalculationList()

    def __init__(self, instrument=None, *args, **kwargs):
        self.instrument = instrument
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(CalculationSet, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if not self.instrument:
            return

        validate_instrument_version(
            self.instrument,
            cstruct,
            node.get('instrument'),
        )

        calculation_ids = set([
            calc['id']
            for calc in cstruct['calculations']
        ])
        instrument_ids = set([
            field['id']
            for field in self.instrument['record']
        ])
        duped = calculation_ids & instrument_ids
        if duped:
            raise ValidationError(
                node.get('calculations'),
                'Calculation IDs cannot be the same as Instrument Field IDs:'
                ' %s' % (
                    ', '.join(duped),
                ),
            )

