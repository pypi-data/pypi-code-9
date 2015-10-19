from district42 import SchemaType
from .abstract_validator import AbstractValidator
from .abstract_formatter import AbstractFormatter
from .validator import Validator
from .formatter import Formatter
from .errors import *


SchemaType.__eq__ = lambda self, other: Validator(Formatter()).validate(other, self).passes()
