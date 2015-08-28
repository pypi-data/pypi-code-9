"""Contains the primitives for building up EBNF parsers."""

import string
from collections import namedtuple
from enum import Enum
from functools import partial


class DeadEnd(Exception):
  """Primitives raise this exception type when they are unable to process a text."""
  pass


class NodeType(Enum):
  """Basic EBNF Node Types."""
  terminal = 1
  concatenation = 2
  repetition = 3
  option = 4


NodeWalkResult = namedtuple("NodeWalkResult", ["node", "parent", "index"])


class Node(object):
  """A Node is the result of a primitive call."""
  def __init__(self, node_type, children=None, consumed=None, position=None, ignored=None):
    """Initialize the Node instance."""
    self.node_type = node_type
    self.children = children or []
    self.position = position
    self.ignored = ignored

    if consumed is None:
      if children:
        self.consumed = sum(c.consumed for c in children)
      else:
        self.consumed = 0
    else:
      self.consumed = consumed

    if ignored is None:
      if children and isinstance(children[0], Node):
        self.ignored = children[0].ignored

    if position is None:
      if children and isinstance(children[0], Node):
        self.position = children[0].position

  @property
  def is_value(self):
    """Returns True if this node has a single string child."""
    return len(self.children) == 1 and isinstance(self.children[0], str)

  @property
  def value(self):
    """Returns the first child."""
    return self.children[0]

  @property
  def svalue(self):
    """Returns the first child, with whitespace stripped."""
    return self.value.strip()

  def add_ignored(self, ignored):
    """Prepend a string to self.ignored and adjust self.consumed appropriately."""
    if ignored:
      if self.ignored:
        self.ignored = ignored + self.ignored
      else:
        self.ignored = ignored

      self.consumed += len(ignored)

  def merge(self, other):
    """Create and return a new node containing all the children of this node and the other, with
    the type of this node.
    """
    children = [c for c in self.children + other.children if len(c) > 0]
    return Node(self.node_type,
                children=children,
                consumed=self.consumed + other.consumed)

  def reconstruct(self, *, include_ignored=False):
    """Reconstructs, as well as possible, the original text that makes up the mode."""
    if self.is_value:
      if include_ignored:
        return (self.ignored or "") + self.value
      else:
        return self.value
    else:
      return "".join(c.reconstruct(include_ignored=include_ignored) for c in self.children)

  def flatten(self, predicate):
    """Recursively flatten a node. This allows us to, for example, hoist up a nested structure
    like a + (b + (c + d)) to a + b + c + d.

    Predicate is a function that takes as arguments the child node and current node, and should
    return True if the child should be flattened into its parent, or False if not.
    """
    idx = 0
    while idx < len(self.children):
      child = self.children[idx]
      if isinstance(child, Node):
        child.flatten(predicate)
        if predicate(child, self):
          self.children[idx:idx + 1] = child.children
          self.consumed += child.consumed
          continue
      idx += 1
    return self

  def trim(self, predicate):
    """Recursively trims nodes from the tree based on a predicate."""
    idx = 0
    while idx < len(self.children):
      child = self.children[idx]
      if isinstance(child, Node):
        child.trim(predicate)

        if predicate(child):
          self.children.pop(idx)
          idx -= 1

      idx += 1

  def is_type(self, value):
    """Returns true if instance's node_type == value.

    If value is a tuple, list, or set each item will be checked in turn against the instance's
    node_type and True will be returned if any match.
    """
    if isinstance(value, (tuple, list, set)):
      for opt in value:
        if self.node_type == opt:
          return True
      return False
    else:
      return self.node_type == value

  def walk(self, *, parent=None, index=None):
    """Yield a 3-tuple of (node, parent, index) for this node and every node that descends
    from it.

    index is a tuple containing the index of each ancestor, from the root to the parent.
    """
    if not index:
      index = (0, )
    yield NodeWalkResult(self, parent, index)
    for idx, child in enumerate(self.children):
      if isinstance(child, Node):
        yield from child.walk(parent=self, index=index + (idx, ))
      else:
        yield NodeWalkResult(child, self, index + (idx, ))

  def __str__(self):
    """Returns a string representation of the node."""
    return self.reconstruct()

  def __repr__(self):
    """Returns a representation of the node."""
    return "({0}, ({1}), {2})".format(
      self.node_type,
      ", ".join(repr(c) for c in self.children if len(c) > 0),
      self.consumed)

  def __eq__(self, other):
    """Returns true if both operands are Nodes and the node_type, amount of text consumed, and
    children are all the same."""
    return isinstance(other, Node) \
           and self.node_type == other.node_type \
           and self.consumed == other.consumed \
           and self.children == other.children

  def __len__(self):
    """Returns the length of the node's children list."""
    return len(self.children)

  @staticmethod
  def iterate(token_type, gen, text):
    """Generate nodes whose node_type is token_type, and whose only child is a result pulled from
    gen(text).
    """
    for node in _iterate(gen(text)):
      yield Node(token_type, [node])

  @staticmethod
  def iterate_merge(token_type, gen, text):
    """Generate nodes whose node_type is token_type, and whose children are merged from the nodes
    generated by gen(text).

    This is useful for renaming a concatenation.
    """
    for node in _iterate(gen(text)):
      if node.node_type in (NodeType.concatenation, NodeType.repetition, NodeType.option):
        yield Node(token_type).merge(node)
      else:
        yield Node(token_type, [node])

  @staticmethod
  def iterate_reduce(token_type, gen, text, *, include_ignored=True):
    """Generate nodes whose node_type is token_type, and whose child is the reconstructed value from
    a node generated by gen(text).

    This is useful for pulling together terminals into identifiers, for example.
    """
    for node in _iterate(gen(text)):
      value = node.reconstruct(include_ignored=include_ignored)
      yield Node(token_type,
                 children=[value],
                 consumed=len(value),
                 ignored=node.ignored if not include_ignored else None,
                 position=node.position)


def pprint(root, depth=0, space_unit="    ", *, source_len=0):
  """Pretty print a node tree, string with root."""
  spacing = space_unit * depth

  if isinstance(root, Node):
    if root.is_value:
      print("{0}{1} (@{2}):\t{3}".format(spacing,
                                         root.node_type,
                                         source_len - root.position,
                                         root.value.strip()))
    else:
      print("{0}{1} (@{2}):".format(spacing,
                                    root.node_type,
                                    source_len - root.position))
      for child in root.children:
        pprint(child, depth + 1, space_unit, source_len=source_len)
  else:
    print("{0}•{1}".format(spacing, str(root)))


def pprint_table(root, depth=0, space_unit="    ", *, source_len=0):
  """Prints out the parse tree in a tabular format."""
  lines = list(_pprint_table_lines(root, depth, space_unit, source_len=source_len))
  mw0 = max(len(l) for l, c, r in lines)
  mw1 = max(len(str(c)) for l, c, r in lines)
  fmt = "{0:" + str(mw0) + "} {1:" + str(mw1) + "} {2}"
  for l, c, r in lines:
    print(fmt.format(l, "" if c is None else c, r or ""))


def _pprint_table_lines(root, depth=0, space_unit="    ", *, source_len):
  """Generates the rows for a pprint_table.

  Each row is a 3-tuple of node_type, source position, value (if any)).
  """
  spacing = space_unit * depth

  if isinstance(root, Node):
    if root.is_value:
      yield ("{0}{1}".format(spacing, root.node_type), source_len - root.position, root.value.strip())
    else:
      yield ("{0}{1}".format(spacing, root.node_type), source_len - root.position, None)
      for child in root.children:
        yield from _pprint_table_lines(child, depth + 1, space_unit, source_len=source_len)
  else:
    yield ("{0}•{1}".format(spacing, str(root)), None, None)


def _iterate(gen):
  """Iterate passes on DeadEnds."""
  while True:
    try:
      yield next(gen)
    except DeadEnd:
      continue


# primitives to support:
# • terminal
# • concatenation
# • alternation
# • repetition (bounded and unbounded)
# • option
# • exclusion


def get_terminal(value, text):
  """Try to get an exact value from the beginning of the text.

  If the value is matched, then a Node with type="terminal", children=[value] and consumed=skipped
  leading characters + len(value) is returned.

  Otherwise DeadEnd is raised.
  """
  if not text:
    raise DeadEnd()

  if text[:len(value)] == value:

    yield Node(NodeType.terminal,
               children=[value],
               consumed=len(value),
               position=len(text))

  raise DeadEnd()


def _count_leading_ws(text):
  """Returns the number of characters at the start of text that are whitespace."""
  i = 0
  for i, c in enumerate(text):
    if not c.isspace():
      return i
  return i + 1


def get_concatenation(extractors, ignore_ws, text):
  """Get a concatenation of extractors from the text.

  This method will generate all possible valid value combinations from the given extractors using
  a depth first search.
  """
  extractor, *remaining = extractors

  # If we ignore whitespace, we will add it to the first returned node after the fact. We'll send
  # to the first extractor the stripped text, but we need to send to the remaining extractors the
  # original text, since we're offsetting it by node.consumed which will include the leading
  # whitespace that was taken
  if ignore_ws:
    leading_ws_count = _count_leading_ws(text)
    ignored_ws = text[:leading_ws_count]
    first_text = text[leading_ws_count:]
  else:
    first_text = text
    ignored_ws = None

  candidates = _iterate(extractor(first_text))

  while True:
    try:
      node = Node(NodeType.concatenation, [next(candidates)])
      node.add_ignored(ignored_ws)
    except StopIteration:
      break

    if remaining:
      for next_node in _iterate(get_concatenation(remaining, ignore_ws, text[node.consumed:])):
        yield node.merge(next_node)
    else:
      yield node

  raise DeadEnd()


def get_alternation_fifo(extractors, text):
  """For each extractor, generate each valid result from the beginning of the text. The extractors
  are exhausted in the order they are specified.
  """
  for _, extractor in enumerate(extractors):
    candidates = _iterate(extractor(text))

    while True:
      try:
        yield next(candidates)
      except StopIteration:
        break

  raise DeadEnd()


def get_alternation_lifo(extractors, text):
  """For each extractor, generate each valid result from the beginning of the text. Each extractor
  is run once, and then exhausted starting from the last back to the first.
  """
  extractor, *remaining = extractors
  candidates = _iterate(extractor(text))
  more = True

  try:
    yield next(candidates)
  except StopIteration:
    more = False

  if remaining:
    yield from get_alternation_lifo(remaining, text)

  while more:
    try:
      yield next(candidates)
    except StopIteration:
      more = False

  raise DeadEnd()


get_alternation = get_alternation_lifo


def get_repetition(extractor, text, *, bound=-1):
  """Extract multiple instances of an extractor from the text. If bound is given, exactly that many
  repetitions will be extracted. If get_repetition is unable to get that many, it will raise a
  DeadEnd exception. If bound is -1 (the default), get_repetition will extract as many repetitions
  as it can find.
  """
  if bound == 0:
    yield Node(NodeType.repetition)
  else:
    candidates = _iterate(extractor(text))
    while True:
      try:
        node = Node(NodeType.repetition, [next(candidates)])
        if node.consumed == 0:
          raise StopIteration
        yield node.merge(next(get_repetition(extractor, text[node.consumed:], bound=bound - 1 if bound > 0 else bound)))
      except StopIteration:
        if bound == -1:
          yield Node(NodeType.repetition)
          break
        else:
          raise DeadEnd()


def get_option(extractor, text):
  """Try to get a single repetition of the extractor from the text."""
  candidates = _iterate(extractor(text))

  while True:
    try:
      yield Node(NodeType.option, [next(candidates)])
    except StopIteration:
      break

  yield Node(NodeType.option)


def get_exclusion(extractor, exclusion, text):
  """Yields each candidate from extractor that is not found in exclusion."""
  candidates = _iterate(extractor(text))
  exclusions = list(_iterate(exclusion(text)))

  while True:
    try:
      node = next(candidates)
      if node not in exclusions:
        yield node
    except StopIteration:
      break

  raise DeadEnd()


def terminal(value):
  """Returns a partial of get_terminal that is ready to accept text as its only argument."""
  return partial(get_terminal, value)


def concatenation(extractors, ignore_ws=True):
  """Returns a partial of get_concatenation that is ready to accept text as its only argument."""
  return partial(get_concatenation, extractors, ignore_ws)


def alternation(extractors):
  """Returns a partial of get_alternation that is ready to accept text as its only argument."""
  return partial(get_alternation, extractors)


def repetition(extractor, *, bound=-1):
  """Returns a partial of get_repetition that is ready to accept text as its only argument."""
  return partial(get_repetition, extractor, bound=bound)


def option(extractor):
  """Returns a partial of get_option that is ready to accept text as its only argument."""
  return partial(get_option, extractor)


def exclusion(extractor, exclusion):
  """Returns a partial of get_exclusion that is ready to accept text as its only argument."""
  return partial(get_exclusion, extractor, exclusion)
