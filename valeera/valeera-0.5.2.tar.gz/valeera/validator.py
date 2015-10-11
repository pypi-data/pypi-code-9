from .abstract_validator import AbstractValidator
from .validator_visitor import ValidatorVisitor
from .pointer import Pointer


class Validator(AbstractValidator):

  def __init__(self, formatter = None):
    super().__init__()
    self._formatter = formatter

  def errors(self):
    if self._formatter is None:
      return self._errors
    return [error.format(self._formatter) for error in self._errors]

  def validate(self, actual, expected):
    self._errors = expected.accept(ValidatorVisitor(), Pointer(actual))
    return self
