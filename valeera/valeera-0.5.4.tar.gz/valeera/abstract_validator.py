class AbstractValidator:

  def __init__(self):
    self._errors = []

  def validate(self, actual, expected):
    raise NotImplementedError()

  def passes(self):
    return len(self._errors) == 0

  def fails(self):
    return len(self._errors) != 0

  def errors(self):
    return self._errors
