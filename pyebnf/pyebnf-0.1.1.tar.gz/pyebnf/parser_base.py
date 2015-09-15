"""Contains the ParserBase class and several utility functions for Parsers."""

import string

from .exception import DeadEnd, ParserError
from .primitive import alternation


# Alternations for the common character classes.
get_ascii_letter = alternation(string.ascii_letters)
get_ascii_lowercase = alternation(string.ascii_lowercase)
get_ascii_uppercase = alternation(string.ascii_uppercase)
get_digit = alternation(string.digits)
get_hexdigit = alternation(string.hexdigits)
get_octdigit = alternation(string.octdigits)
get_printable = alternation(string.printable)
get_punctuation = alternation(string.punctuation)
get_whitespace = alternation(string.whitespace)


class ParserBase(object):
  """Base class for Parsers."""
  entry_point = None

  def __init__(self):
    """Initialize the Parser instance."""
    self.most_consumed = 0
    self.original_text = None

  def parse(self, text):
    """Attempt to parse source code."""
    self.original_text = text

    try:
      return getattr(self, self.entry_point)(text)
    except (DeadEnd) as exc:
      raise ParserError(self.most_consumed, "Failed to parse input") from exc
    return tree

  def _attempting(self, text):
    """Keeps track of the furthest point in the source code the parser has reached to this point."""
    consumed = len(self.original_text) - len(text)
    self.most_consumed = max(consumed, self.most_consumed)

  def _special_handling_default(self, value):
    """A special default callout for special handling."""
    raise NotImplementedError("Special handling {0} not yet implemented".format(value))
