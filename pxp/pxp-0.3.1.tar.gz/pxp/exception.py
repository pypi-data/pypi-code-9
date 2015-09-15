class PXPError(Exception):
  """Base class for all PXPErrors."""
  pass


class ScopeError(PXPError):
  """Error type thrown by pxp.source.SourceBase classes."""
  pass


class PositionalError(PXPError):
  """Position error type. Contains a source-code position accompanying the error."""
  def __init__(self, position, *args):
    """Initializes the PositionalError instance."""
    super().__init__(*args)
    self.position = position

  def __str__(self):
    """The string representation of the error with the message and the 1-based coordinates of the
    position.
    """
    return "{0} at position {1}".format(self.message, self.position1)

  @property
  def message(self):
    """The error message."""
    return super().__str__()

  @property
  def position1(self):
    """The 1-based position of the offending code."""
    line, char = self.position
    return (line + 1, char + 1)


class CompilerError(PositionalError):
  """Error type thrown by the Compiler."""
  pass


class RuntimeError(PositionalError):
  """Error type thrown by the runtime (interpreter)."""
  pass


class FunctionError(PXPError):
  """Error type thrown by functions."""
  pass


class OperatorError(FunctionError):
  """Error type thrown by operators."""
  pass
