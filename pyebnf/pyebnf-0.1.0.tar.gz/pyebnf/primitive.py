"""Contains primitives for building EBNF parsers."""

import itertools
from enum import Enum
from functools import partial

from .exception import DeadEnd


class ParseNodeType(Enum):
  """This enum represents the distinct types that ParseNodes can represent."""
  terminal = 1
  concatenation = 2
  repetition = 3


def flattened_pred_default(node, parent):
  """The default predicate used in Node.flattened."""
  return isinstance(node.node_type, ParseNodeType)


def trimmed_pred_default(node, parent):
  """The default predicate used in Node.trimmed."""
  return isinstance(node, ParseNode) and (node.is_empty or node.is_type(ParseNodeType.terminal))


class ParseNode(object):
  """A ParseNode is a node in a ParserTree that has a type, and one or more children. The children
  can either be 1 or more ParseNodes, or a single string. It also keeps track of it's position
  in the original text. If position is a negative number, it is the node's position from the end
  of the text.
  """
  def __init__(self, node_type, *, children=None, consumed=None, position=None, ignored=None):
    """Initializes the ParseNode instance."""
    self.node_type = node_type
    self.children = tuple(children or [])
    self._position = position
    self.ignored = ignored

    if consumed is None:
      if children:
        self.consumed = sum(c.consumed for c in children)
      else:
        self.consumed = 0
    else:
      self.consumed = consumed

  @property
  def position(self):
    """Gets the position of the text the ParseNode processed. If the ParseNode does not have its
    own position, it looks to its first child for its position.

    'Value Nodes' (terminals) must have their own position, otherwise this method will throw an
    exception when it tries to get the position property of the string child.
    """
    pos = self._position
    if pos is None and self.children:
      ch1 = self.children[0]
      if isinstance(ch1, ParseNode):
        pos = ch1.position
    return pos

  @property
  def is_empty(self):
    """Returns True if this node has no children, or if all of its children are ParseNode instances
    and are empty.
    """
    return all(isinstance(c, ParseNode) and c.is_empty for c in self.children)

  @property
  def is_value(self):
    """Returns true if the node has a single child and it is a string."""
    return len(self.children) == 1 and isinstance(self.children[0], str)

  @property
  def value(self):
    """Returns the first child. This method should only be used when is_value returns True."""
    return self.children[0]

  @property
  def svalue(self):
    """Returns the value with all whitespace stripped. This method should only be called if is_value
    returns True.
    """
    return self.value.strip()

  def add_ignored(self, ignored):
    """Add ignored text to the node. This will add the length of the ignored text to the node's
    consumed property.
    """
    if ignored:
      if self.ignored:
        self.ignored = ignored + self.ignored
      else:
        self.ignored = ignored

    self.consumed += len(ignored)

  def is_type(self, value):
    """Returns True if node_type == value.

    If value is a tuple, node_type is checked against each member and True is returned if any of
    them match.
    """
    if isinstance(value, tuple):
      for opt in value:
        if self.node_type == opt:
          return True
      return False
    else:
      return self.node_type == value

  def flattened(self, pred=flattened_pred_default):
    """Flattens nodes by hoisting children up to ancestor nodes.

    A node is hoisted if pred(node) returns True.
    """
    if self.is_value:
      return self

    new_children = []

    for child in self.children:
      if child.is_empty:
        continue

      new_child = child.flattened(pred)

      if pred(new_child, self):
        new_children.extend(new_child.children)
      else:
        new_children.append(new_child)

    return ParseNode(self.node_type,
                     children=new_children,
                     consumed=self.consumed,
                     position=self.position,
                     ignored=self.ignored)

  def trimmed(self, pred=trimmed_pred_default):
    """Trim a ParseTree.

    A node is trimmed if pred(node) returns True.
    """
    new_children = []

    for child in self.children:
      if isinstance(child, ParseNode):
        new_child = child.trimmed(pred)
      else:
        new_child = child

      if not pred(new_child, self):
        new_children.append(new_child)

    return ParseNode(self.node_type,
                     children=new_children,
                     consumed=self.consumed,
                     position=self.position,
                     ignored=self.ignored)

  def merged(self, other):
    """Returns a new ParseNode whose type is this node's type, and whose children are all the
    children from this node and the other whose length is not 0.
    """
    children = [c for c in itertools.chain(self.children, other.children) if len(c) > 0]
    # NOTE: Only terminals should have ignored text attached to them, and terminals shouldn't be
    #       merged (probably) so it shouldn't be necessary to copy of ignored -- it should always
    #       be None. But, we'll go ahead and copy it over anyway, recognizing that other's
    #       ignored text will be lost.
    return ParseNode(self.node_type,
                      children=children,
                      consumed=self.consumed + other.consumed,
                      ignored=self.ignored)

  def retyped(self, new_type):
    """Returns a new node with the same contents as self, but with a new node_type."""
    return ParseNode(new_type,
                      children=list(self.children),
                      consumed=self.consumed,
                      position=self.position,
                      ignored=self.ignored)

  def compressed(self, new_type=None, *, include_ignored=False):
    """Turns the node into a value node, whose single string child is the concatenation of all its
    children.
    """
    values = []
    consumed = 0
    ignored = None

    for i, child in enumerate(self.children):
      consumed += child.consumed
      if i == 0 and not include_ignored:
        ignored = child.ignored
      if child.is_value:
        if include_ignored:
          values.append("{0}{1}".format(child.ignored or "", child.value))
        else:
          values.append(child.value)
      else:
        values.append(child.compressed(include_ignored=include_ignored).value)

    return ParseNode(new_type or self.node_type,
                      children=["".join(values)],
                      consumed=consumed,
                      ignored=ignored,
                      position=self.position)

  def __len__(self):
    """This method returns the length of all the unignored text this node and its descendants."""
    return sum(len(c) for c in self.children)

  def __lshift__(self, other):
    """This method calls through to merged."""
    return self.merged(other)

  def __eq__(self, other):
    """Checks that two nodes are exactly the same on all properties."""
    return self.node_type == other.node_type and \
           self.children == other.children and \
           self.position == other.position and \
           self.ignored == other.ignored

  def __repr__(self):
    """Returns a representation of the node."""
    return """({0}, {1}, {2}, {3}, "{4}")""".format(self.node_type,
                                                    repr(self.children),
                                                    self.position,
                                                    self.consumed,
                                                    self.ignored or "")


def pprint(root, depth=0, space_unit="    ", *, source_len=0, file=None):
  """Pretting print a parse tree."""
  spacing = space_unit * depth

  if isinstance(root, str):
    print("{0}terminal@(?): {1}".format(spacing, root), file=file)
  else:
    if root.position is None:
      position = -1
    elif root.position < 0:
      position = source_len + root.position
    else:
      position = root.position

    if root.is_value:
      print("{0}{1}@({2}:{3}):\t{4}".format(spacing, root.node_type, position, root.consumed, root.svalue), file=file)
    else:
      print("{0}{1}@({2}:{3}):".format(spacing, root.node_type, position, root.consumed), file=file)
      for child in root.children:
        pprint(child, depth + 1, source_len=source_len, file=file)


# primitives to support:
# • terminal
# • concatenation
# • alternation
# • repetition (option, zero or more, one or more, exact repeat, arbitrarily bounded)
# • exclusion


def terminal(value):
  """Returns a partial of _get_terminal that accepts only a text argument."""
  return partial(_get_terminal, value)


def concatenation(extractors, *, ignore_whitespace=True):
  """Returns a partial of _get_concatenation that accepts only a text argument."""
  return partial(_get_concatenation, extractors, ignore_whitespace=ignore_whitespace)


def alternation(extractors):
  """Returns a partial of _get_alternation that accepts only a text argument."""
  return partial(_get_alternation, extractors)


def option(extractor):
  """Returns a partial of _get_repetition with bounds set to (0, 1) that accepts only a text
  argument.
  """
  return partial(_get_repetition, extractor, bounds=(0, 1))


def zero_or_more(extractor, *, ignore_whitespace=False):
  """Returns a partial of _get_repetition with bounds set to (0, None) that accepts only a text
  argument.
  """
  return partial(_get_repetition, extractor, bounds=(0, None), ignore_whitespace=ignore_whitespace)


def one_or_more(extractor, *, ignore_whitespace=False):
  """Returns a partial of _get_repetition with bounds set to (1, None) that accepts only a text
  argument.
  """
  return partial(_get_repetition, extractor, bounds=(1, None), ignore_whitespace=ignore_whitespace)


def repeated(extractor, times, *, ignore_whitespace=False):
  """Returns a partial of _get_repetition with bounds set to (times, times) that accepts only a text
  argument.
  """
  return partial(_get_repetition,
                 extractor,
                 bounds=(times, times),
                 ignore_whitespace=ignore_whitespace)


def repetition(extractor, bounds, *, ignore_whitespace=False):
  """Returns a partial of _get_repetition that accepts only a text argument."""
  return partial(_get_repetition, extractor, bounds=bounds, ignore_whitespace=ignore_whitespace)


def exclusion(extractor, exclusion):
  """Returns a partial of _get_exclusion that accepts only a text argument."""
  return partial(_get_exclusion, extractor, exclusion)


def _get_terminal(value, text):
  """Checks the beginning of text for a value. If it is found, a terminal ParseNode is returned
  filled out appropriately for the value it found. DeadEnd is raised if the value does not match.
  """
  if text and text.startswith(value):
    return ParseNode(ParseNodeType.terminal,
                      children=[value],
                      consumed=len(value),
                      position=-len(text))
  else:
    raise DeadEnd()


def _get_concatenation(extractors, text, *, ignore_whitespace=True):
  """Returns a concatenation ParseNode whose children are the nodes returned by each of the
  methods in the extractors enumerable.

  If ignore_whitespace is True, whitespace will be ignored and then attached to the child it
  preceeded.
  """
  ignored_ws, use_text = _split_ignored(text, ignore_whitespace)

  extractor, *remaining = extractors

  child = _call_extractor(extractor, use_text)
  child.add_ignored(ignored_ws)

  # TODO: Should I set node.position = -len(text) for the case that ignored whitespace will cause
  #       the first child's position to not be the whitespace, and therefore the concatenation's
  #       position will be the first non-whitespace? I think not, but I'm adding this note in
  #       case that causes an issue I'm not seeing at the moment.
  node = ParseNode(ParseNodeType.concatenation, children=[child])

  if remaining:
    # child.consumed will include ignored whitespace, so we base the text we pass on on text rather
    # than use_text.
    return node.merged(_get_concatenation(remaining,
                                          text[child.consumed:],
                                          ignore_whitespace=ignore_whitespace))
  else:
    return node


def _get_alternation(extractors, text):
  """Tries each extractor on the given text and returns the 'best fit'.

  Best fit is defined by as the extractor whose result consumed the most text. If more than one
  extractor is the best fit, the result of the one that appeared earliest in the list is returned.

  If all extractors raise a DeadEnd, this method too will raise a DeadEnd.
  """
  candidates = []

  for extractor in extractors:
    try:
      candidates.append(_call_extractor(extractor, text))
    except DeadEnd:
      pass

  if not candidates:
    raise DeadEnd

  result, *remaining = candidates

  for candidate in remaining:
    if len(candidate) > len(result):
      result = candidate

  return result


def _get_repetition(extractor, text, *, bounds=(0, None), ignore_whitespace=False):
  """Tries to pull text with extractor repeatedly.

  Bounds is a 2-tuple of (lbound, ubound) where lbound is a number and ubound is a number or None.
  If the ubound is None, this method will execute extractor on text until extrator raises DeadEnd.
  Otherwise, extractor will be called until it raises DeadEnd, or it has extracted ubound times.

  If the number of children extracted is >= lbound, then a ParseNode with type repetition is
  returned. Otherwise, DeadEnd is raised.

  Bounds are interpreted as (lbound, ubound]

  This method is used to implement:
  - option (0, 1)
  - zero_or_more (0, None)
  - one_or_more (1, None)
  - exact_repeat (n, n)
  """
  minr, maxr = bounds
  children = []

  while maxr is None or len(children) <= maxr:
    ignored_ws, use_text = _split_ignored(text, ignore_whitespace)
    try:
      child = _call_extractor(extractor, use_text)
      child.add_ignored(ignored_ws)
    except DeadEnd:
      break

    if child.is_empty:
      break

    children.append(child)
    text = text[child.consumed:]


  if len(children) >= minr:
    return ParseNode(ParseNodeType.repetition,
                      children=children)
  else:
    raise DeadEnd()


def _get_exclusion(extractor, exclusion, text):
  """Returns extractor's result if exclusion does not match.

  If exclusion raises DeadEnd (meaning it did not match) then the result of extractor(text) is
  returned. Otherwise, if exclusion does not raise DeadEnd it means it did match, and we then
  raise DeadEnd.
  """
  try:
    _call_extractor(exclusion, text)
    exclusion_matches = True
  except DeadEnd:
    exclusion_matches = False

  if exclusion_matches:
    raise DeadEnd()
  else:
    return _call_extractor(extractor, text)


def _split_ignored(text, ignore_whitespace=True):
  """Return (leading whitespace, trailing text) if ignore_whitespace is true, or ("", text) if
  False.
  """
  if ignore_whitespace:
    leading_ws_count = _count_leading_whitespace(text)
    ignored_ws = text[:leading_ws_count]
    use_text = text[leading_ws_count:]
    return (ignored_ws, use_text)
  else:
    return ("", text)


def _count_leading_whitespace(text):
  """Returns the number of characters at the beginning of text that are whitespace."""
  idx = 0
  for idx, char in enumerate(text):
    if not char.isspace():
      return idx
  return idx + 1


def _call_extractor(extractor, text):
  """This method calls an extractor on some text.

  If extractor is just a string, it is passed as the first value to _get_terminal. Otherwise it is
  treated as a callable and text is passed directly to it.

  This makes it so you can have a shorthand of terminal(val) <-> val.
  """
  if isinstance(extractor, str):
    return _get_terminal(extractor, text)
  else:
    return extractor(text)
