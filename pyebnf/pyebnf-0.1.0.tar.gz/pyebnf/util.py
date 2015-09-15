"""Contains utility methods used by and with the pyebnf package."""

import math


def esc_split(text, delimiter=" ", maxsplit=-1, escape="\\", *, ignore_empty=False):
  """Escape-aware text splitting:

  Split text on on a delimiter, recognizing escaped delimiters."""
  is_escaped = False
  split_count = 0
  yval = []

  for char in text:
    if is_escaped:
      is_escaped = False
      yval.append(char)
    else:
      if char == escape:
        is_escaped = True
      elif char in delimiter and split_count != maxsplit:
        if yval or not ignore_empty:
          yield "".join(yval)
          split_count += 1
        yval = []
      else:
        yval.append(char)

  yield "".join(yval)


def esc_join(iterable, delimiter=" ", escape="\\"):
  """Join an iterable by a delimiter, replacing instances of delimiter in items
  with escape + delimiter.
  """
  rep = escape + delimiter
  return delimiter.join(i.replace(delimiter, rep) for i in iterable)


def get_newline_positions(text):
  """Returns a list of the positions in the text where all new lines occur. This is used by
  get_line_and_char to efficiently find coordinates represented by offset positions.
  """
  pos = []
  for i, c in enumerate(text):
    if c == "\n":
      pos.append(i)
  return pos


def get_line_and_char(newline_positions, position):
  """Given a list of newline positions, and an offset from the start of the source code
  that newline_positions was pulled from, return a 2-tuple of (line, char) coordinates.
  """
  if newline_positions:
    for line_no, nl_pos in enumerate(newline_positions):
      if nl_pos >= position:
        if line_no == 0:
          return (line_no, position)
        else:
          return (line_no, position - newline_positions[line_no - 1] - 1)
    return (line_no + 1, position - newline_positions[-1] - 1)
  else:
    return (0, position)


def point_to_source(source, position, fmt=(2, True, "~~~~~", "^")):
  """Point to a position in source code.

  source is the text we're pointing in.
  position is a 2-tuple of (line_number, character_number) to point to.
  fmt is a 4-tuple of formatting parameters, they are:
    name               default  description
    ----               -------  -----------
    surrounding_lines  2        the number of lines above and below the target line to print
    show_line_numbers  True     if true line numbers will be generated for the output_lines
    tail_body          "~~~~~"  the body of the tail
    pointer_char       "^"      the character that will point to the position
  """

  surrounding_lines, show_line_numbers, tail_body, pointer_char = fmt

  line_no, char_no = position

  lines = source.split("\n")
  line = lines[line_no]

  if char_no >= len(tail_body):
    tail = " " * (char_no - len(tail_body)) + tail_body + pointer_char
  else:
    tail = " " * char_no + pointer_char + tail_body

  if show_line_numbers:
    line_no_width = int(math.ceil(math.log10(max(1, line_no + surrounding_lines))) + 1)
    line_fmt = "{0:" + str(line_no_width) + "}: {1}"
  else:
    line_fmt = "{1}"

  pivot = line_no + 1
  output_lines = [(pivot, line), ("", tail)]
  for i in range(surrounding_lines):
    upper_ofst = i + 1
    upper_idx = line_no + upper_ofst
    lower_ofst = -upper_ofst
    lower_idx = line_no + lower_ofst

    if lower_idx >= 0:
      output_lines.insert(0, (pivot + lower_ofst, lines[lower_idx]))
    if upper_idx < len(lines):
      output_lines.append((pivot + upper_ofst, lines[upper_idx]))

  return "\n".join(line_fmt.format(n, c) for n, c in output_lines)
