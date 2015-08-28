"""Contains the ParserBase class and several utility functions for Parsers."""

import string
from itertools import repeat

from .exception import ParserError
from .primitive import get_alternation, terminal


def get_printable_character(text):
  """Special handling for printable_character, since this is so common."""
  yield from get_alternation((terminal(c) for c in string.printable), text)


def get_whitespace_character(text):
  """Special handling for whitespace_character, since this is so common."""
  yield from get_alternation((terminal(c) for c in string.whitespace), text)


class ParserBase(object):
  """Base class for Parsers."""
  def __init__(self):
    """Initialize the Parser instance."""
    self.most_consumed = 0
    self.original_text = None

  def attempting(self, text):
    """Keeps track of the furthest point in the source code the parser has reached to this point."""
    consumed = len(self.original_text) - len(text)
    self.most_consumed = max(consumed, self.most_consumed)

  def parse(self, text):
    """Attempt to parse source code."""
    self.original_text = text

    try:
      return next(self.entry_point(text))
    except (RuntimeError, StopIteration) as exc:
      raise ParserError(self.most_consumed, "Failed to parse input") from exc
    return tree

  def merged(self, node_type, gen, text):
    """A shortcut to Node.iterate_merge."""
    yield from Node.iterate_merge(node_type, gen, text)

  def special_handling_default(self, value):
    """A special default callout for special handling."""
    raise NotImplementedError("Special handling {0} not yet implemented".format(value))

  def entry_point(self, text):
    """The entry_point for the parser. Must be overidden by subclasses."""
    raise NotImplementedError()
