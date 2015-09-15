"""Contains the exceptions thrown by the pyebnf package."""

class PyEBNFError(Exception):
  """Base class for all Exceptions thrown by the pyebnf package."""
  pass


class DeadEnd(PyEBNFError):
  """Primitives throw this error when they cannot process the text they're given."""
  pass


class ParserError(PyEBNFError):
  """Exception thrown by Parser when it is unable to parse some source."""
  def __init__(self, position, *args):
    """Initialize the ParserError instance."""
    super().__init__(*args)
    self.position = position

  def __str__(self):
    """Returns a string representation of the ParserError instance."""
    return "{0} at position {1}".format(self.message, self.position)

  @property
  def message(self):
    """Returns just the error message."""
    return super().__str__()


class CompilerError(PyEBNFError):
  """Thrown by the compiler module when it experiences an issue."""
  pass


class OperatorError(CompilerError):
  """Thrown by the operator module when it experiences an issue."""
  pass
