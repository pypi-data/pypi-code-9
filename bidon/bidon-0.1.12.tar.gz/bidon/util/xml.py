"""Methods for transforming xml.ElementTree nodes."""


def get_text(element):
  """Returns the text of element."""
  return element.text


def get_attribute(element, name):
  """Returns an attribute from an element."""
  return element.attrib[name]


def to_dict(element, transform_def):
  """Transform an element into a dict.

  transform_def is a dict. The return value's keys will match transform_def, and the values will
  be the result from transform(element, transform_def[key]).
  """
  return {k: transform(element, a) for k, a in transform_def.items()}


def transform(element, method=None):
  """A flexible element transformer.

  method can be one of 5 types: None, str, dict, tuple, callable. The behaviors are as follows:

  None - return the text of the element
  str - return the attribute of the element whose name matches the argument
  dict - transform the element into a dict, whose keys are the keys of the given dict, and whose
         values are the result from passing the element and the parameter dict's value to this
         function.
  tuple - call transform on one or more children. The tuple can be either a 1-tuple, 2-tuple or
          3-tuple. They are translated as follows:

          (xpath[, method[, index]])

          xpath - the xpath expression to get the children from the element
          method - any value that can be passed as this function's `method` argumet. Defaults to
                   None
          index - either the string '*' or a child index or None. Defaults to 0. If index is '*',
                  then the result will be a list using all the children found by xpath. If the index
                  is None, then xpath is interpreted instead as an attribute reference. This allows
                  you to pass in callables for the method to be called on attributes.
  callable - returns the result of method(element)
  """
  # pylint: disable=too-many-return-statements

  if method is None:
    return get_text(element)

  elif isinstance(method, str):
    return get_attribute(element, method)

  elif isinstance(method, dict):
    return to_dict(element, method)

  elif isinstance(method, tuple) and len(method) in (1, 2, 3):
    if len(method) == 1:
      xpath = method[0]
      method_ = None
      index = 0

    elif len(method) == 2:
      xpath, method_ = method
      index = 0

    else:
      xpath, method_, index = method

    try:
      if index == "*":
        return list(transform_all(element.findall(xpath), method_))
      elif index is None:
        raw_val = get_attribute(element, xpath)
        return raw_val if method_ is None else method_(raw_val)
      else:
        return transform(element.findall(xpath)[index], method_)
    except Exception as ex:
      raise Exception("An error occurred with path {}".format(xpath)) from ex

  elif callable(method):
    return method(element)

  else:
    raise ValueError("Unrecognized transformation method")


def transform_all(elements, method):
  """Generates a sequence of transformed elements."""
  for element in elements:
    yield transform(element, method)
