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
    def __init__(self, expression, index, format_spec, conversion, args, kwargs):
        self.expression = expression

        self.positions = {}
        self.add_position(index, format_spec, conversion)

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

    def format_list(self, value, index):
        format_spec, conversion = self.positions[index]
        if conversion == 'r':
            return self.format_standard(value, index)
        else:
            conversion = 's'

        value = tuple(value)
        last = _formatter.convert_field(value[-1], conversion)

        if len(value) > 1:
            other = []
            for item in value[:-1]:
                item = _formatter.convert_field(item, conversion)
                other.append(item)

            value = '"' + '", "'.join(other) + '" and "' + last + '"'
        else:
            value = last

        try:
            return _formatter.format_field(value, format_spec)
        except:
            return self.restore_field(index)

    def format_plural(self, index):
        format_spec, conversion = self.positions[index]
        if isinstance(self.plural_subject.value, (tuple, set, list)):
            number = len(self.plural_subject.value)
        else:
            number = self.plural_subject.value

        if number != 1:
            value = self.plural_options[0]
        else:
            if len(self.plural_options) > 1:
                value = self.plural_options[1]
            else:
                value = ''

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

def _parse_format(string, args, kwargs):
    sequence = []
    expressions = {}

    current = 0
    for field in _formatter.parse(string):
        literal, expression, format_spec, conversion = field
        if literal:
            sequence.append(literal)

        if isinstance(expression, types.StringTypes):
            if not expression:
                expression = str(current)
                current += 1

            sequence.append(None)
            index = len(sequence) - 1
            if expression in expressions:
                expressions[expression].add_position(index, format_spec, conversion)
            else:
                expressions[expression] = _Expression(expression, index, format_spec, conversion, args, kwargs)

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
