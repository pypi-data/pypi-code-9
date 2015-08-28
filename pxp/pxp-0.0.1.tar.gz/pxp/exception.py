class PXPError(Exception):
  pass


class ScopeError(PXPError):
  pass


class PositionalError(PXPError):
  def __init__(self, position, *args):
    super().__init__(*args)
    self.position = position

  def __str__(self):
    return "{0} at position {1}".format(self.message, self.position1)

  @property
  def message(self):
    return super().__str__()

  @property
  def position1(self):
    """The 1-based position of the offending code."""
    line, char = self.position
    return (line + 1, char + 1)


class CompilerError(PositionalError):
  pass


class RuntimeError(PositionalError):
  pass


class FunctionError(PXPError):
  pass


class OperatorError(FunctionError):
  pass
