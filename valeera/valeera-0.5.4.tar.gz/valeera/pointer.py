class Pointer:

  root = '#'

  def __init__(self, dictionary, path = None):
    self._dictionary = dictionary
    self._path = [] if path is None else path

  def move(self, step):
    return Pointer(self._dictionary, self._path + [step])

  def has_value(self):
    node = self._dictionary
    for step in self._path:
      if (type(step) is int) and (step >= len(node)):
        return False
      elif (type(step) is str) and (step not in node):
        return False
      node = node[step]
    return True

  def value(self):
    node = self._dictionary
    for step in self._path:
      node = node[step]
    return node

  def path(self):
    path = self.root
    for step in self._path:
      path += ('[' + str(step) + ']') if (type(step) is int) else ('.' + step)
    return path
