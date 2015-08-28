"""Contains utility methods used by and with the pyebnf package."""

from functools import wraps


def to_line_and_char(text, idx):
  """Returns the line and column of a character position."""
  last_newline = 0
  newline_count = 0
  next_newline = text.find("\n", last_newline + 1, idx)
  while next_newline != -1:
    last_newline = next_newline
    newline_count += 1
    next_newline = text.find("\n", last_newline + 1, idx)
  return (newline_count + 1, idx - last_newline - 1)


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


_DEBUG_DEPTH = 0
_ITER_ID = 0


def debug_call(*, show_entrance=True, show_args=True, show_exit=True):
  """Decorator creator for printing out function call debug info."""

  def decorator(fxn):
    """Decorator for printing out function call debug info."""

    @wraps(fxn)
    def wrapper(*args, **kwargs):
      """Wrapper for printing out function call debug info."""
      global _DEBUG_DEPTH
      _DEBUG_DEPTH += 1

      if show_entrance:
        if show_args:
          print("  " * _DEBUG_DEPTH + "ENTERED {1}".format(_fxn_call_to_str(fxn, args, kwargs)))
        else:
          print("  " * _DEBUG_DEPTH + "ENTERED {0}".format(fxn.__name__))

      try:
        res = fxn(*args, **kwargs)
        if show_exit:
          print("  " * _DEBUG_DEPTH + "RETURNED {0}".format(res))
        _DEBUG_DEPTH -= 1
        return res

      except Exception as ex:
        print("  " * _DEBUG_DEPTH + "RAISED {0}".format(ex))
        _DEBUG_DEPTH -= 1
        raise

    return wrapper
  return decorator


def debug_iter(*, show_entrance=True, show_args=True, show_exit=True):
  """Decorator creator for printing out iteration call debug info."""

  def decorator(fxn):
    """Decorator for printing out iteration call debug info."""

    @wraps(fxn)
    def wrapper(*args, **kwargs):
      """Wrapper for printing out iteration call debug info."""
      global _ITER_ID
      iter_id = _ITER_ID
      _ITER_ID += 1

      values = fxn(*args, **kwargs)
      i = -1

      while True:
        i = i + 1
        try:
          val = next(values)
          print("{0}#{1}:{2} yielded {3}".format(_fxn_call_to_str(fxn, args, kwargs), iter_id, i, val))
          yield val
        except Exception as ex:
          print("{0}#{1}:{2} raised {3}: {4}".format(_fxn_call_to_str(fxn, args, kwargs), iter_id, i, ex.__class__.__name__, ex))
          raise
    return wrapper
  return decorator


def _fxn_call_to_str(fxn, args, kwargs):
  """Returns a string representation of a function call with args."""
  name = fxn.__name__
  argsa = []
  argsa.extend(str(a) for a in args)
  argsa.extend("{0}={1}".format(k, v) for k, v in kwargs.items())
  return name
