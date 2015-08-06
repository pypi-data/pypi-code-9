import string
import types
import re

_formatter = string.Formatter()

_PLURAL_REGEX = re.compile('(.+)\\_plural(\\<([^\\>]+)\\>)?$')

def _parse_expression(expression):
    match = _PLURAL_REGEX.match(expression)
    if not match:
        return None, None

    expression, all_options, options = match.groups()
    if all_options:
        return expression, options.split('|')

    return expression, ['s']

class _Expression(object):
    def __init__(self, expression, args, kwargs):
        self.expression = expression

        self.positions = {}
        try:
            value, name = _formatter.get_field(expression, args, kwargs)
        except:
            pass
        else:
            self.value = value
            self.name = name

    def add_position(self, index, format_spec, conversion):
        self.positions[index] = (format_spec, conversion)

    def try_set_plural(self):
        if hasattr(self, 'value'):
            return False

        expression, options = _parse_expression(self.expression)
        if expression is None:
            return False

        self.plural_expression = expression
        self.plural_options = options

        return True

    def assign_subject(self, expressions):
        try:
            expression = expressions[self.plural_expression]
        except KeyError:
            return

        if hasattr(expression, 'value') and \
           isinstance(expression.value, (int, long, tuple, set, list)):
            self.plural_subject = expression

    def restore_field(self, index):
        format_spec, conversion = self.positions[index]
        format_spec = ':' + format_spec if format_spec else ''
        conversion = '!' + conversion if conversion else ''

        return '{' + self.expression + conversion + format_spec + '}'

    def format_standard(self, value, index):
        format_spec, conversion = self.positions[index]
        if conversion:
            try:
                value = _formatter.convert_field(value, conversion)
            except:
                return self.restore_field(index)

        try:
            return _formatter.format_field(value, format_spec)
        except:
            return self.restore_field(index)

    @staticmethod
    def convert_list(value, conversion):
        value = tuple(value)
        last = _formatter.convert_field(value[-1], conversion)

        if len(value) > 1:
            other = []
            for item in value[:-1]:
                item = _formatter.convert_field(item, conversion)
                other.append(item)

            return '"' + '", "'.join(other) + '" and "' + last + '"'

        return last

    def format_list(self, value, index):
        format_spec, conversion = self.positions[index]
        if conversion == 'r':
            return self.format_standard(value, index)

        conversion = 's'

        value = self.convert_list(value, conversion)
        try:
            return _formatter.format_field(value, format_spec)
        except:
            return self.restore_field(index)

    @staticmethod
    def get_number(value):
        if isinstance(value, (tuple, set, list)):
            return len(value)

        return value

    def get_option(self, number):
        options = self.plural_options
        if number == 1:
            return options[1] if len(options) > 1 else ''

        return options[0]

    def format_plural(self, index):
        format_spec, conversion = self.positions[index]

        number = self.get_number(self.plural_subject.value)
        value = self.get_option(number)
        try:
            return _formatter.format_field(value, format_spec)
        except:
            return self.restore_field(index)

    def format_field(self, index):
        if hasattr(self, 'value'):
            value = self.value
            if isinstance(value, (tuple, set, list)):
                return self.format_list(value, index)

            return self.format_standard(value, index)

        if hasattr(self, 'plural_subject'):
           return self.format_plural(index) 

        return self.restore_field(index)

    def substitute(self, sequence):
        for index in self.positions:
            sequence[index] = self.format_field(index)

def _append_literal(sequence, literal):
    if literal:
        sequence.append(literal)

def _append_expression(sequence, expressions, expression, args, kwargs,
                       format_spec, conversion):
    sequence.append(None)
    index = len(sequence) - 1

    if expression not in expressions:
        expressions[expression] = _Expression(expression, args, kwargs)
    expressions[expression].add_position(index, format_spec, conversion)

def _parse_format(string, args, kwargs):
    sequence = []
    expressions = {}

    current = 0
    for field in _formatter.parse(string):
        literal, expression, format_spec, conversion = field
        _append_literal(sequence, literal)

        if isinstance(expression, types.StringTypes):
            if not expression:
                expression = str(current)
                current += 1

            _append_expression(sequence, expressions, expression, args, kwargs,
                               format_spec, conversion)

    return sequence, expressions

def _analyse(expressions):
    regular = {}
    plurals = []
    for expression in expressions.keys():
        item = expressions[expression]
        if item.try_set_plural():
            plurals.append(item)
        else:
            regular[expression] = item

    for plural in plurals:
        plural.assign_subject(regular)

def sweeten(*args, **kwargs):
    string = args[0]
    args = args[1:]

    sequence, expressions = _parse_format(string, args, kwargs)
    _analyse(expressions)

    for expression in expressions.itervalues():
        expression.substitute(sequence)

    return reduce(lambda a, b: a + b, sequence)
