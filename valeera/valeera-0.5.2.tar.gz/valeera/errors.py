class ValidationError:
  
  def _get_type_as_string(self, value):
    return str(type(value))[8:-2]


class ValidationTypeError(ValidationError):

  def __init__(self, path, actual_val, expected_types):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.expected_types = expected_types if type(expected_types) is list else [expected_types]

  def format(self, formatter):
    return formatter.format_type_error(self)


class ValidationValueError(ValidationError):

  def __init__(self, path, actual_val, expected_val):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.expected_val = expected_val

  def format(self, formatter):
    return formatter.format_value_error(self)


class ValidationMinValueError(ValidationError):

  def __init__(self, path, actual_val, min_value):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.min_value = min_value
  
  def format(self, formatter):
    return formatter.format_min_value_error(self)


class ValidationMaxValueError(ValidationError):

  def __init__(self, path, actual_val, max_value):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.max_value = max_value
  
  def format(self, formatter):
    return formatter.format_max_value_error(self)


class ValidationRemainderError(ValidationError):

  def __init__(self, path, actual_val, divisor):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.divisor = divisor
  
  def format(self, formatter):
    return formatter.format_remainder_error(self)


class ValidationPatternMismatchError(ValidationError):

  def __init__(self, path, actual_val, pattern):
    self.path = path
    self.actual_val = actual_val
    self.pattern = pattern

  def format(self, formatter):
    return formatter.format_pattern_mismatch_error(self)


class ValidationLengthError(ValidationError):
  
  def __init__(self, path, actual_val, length):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.length = length

  def format(self, formatter):
    return formatter.format_length_error(self)


class ValidationMinLengthError(ValidationError):
  
  def __init__(self, path, actual_val, min_length):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.min_length = min_length

  def format(self, formatter):
    return formatter.format_min_length_error(self)


class ValidationMaxLengthError(ValidationError):
  
  def __init__(self, path, actual_val, max_length):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.max_length = max_length

  def format(self, formatter):
    return formatter.format_max_length_error(self)


class ValidationIndexError(ValidationError):

  def __init__(self, path):
    self.path = path

  def format(self, formatter):
    return formatter.format_index_error(self)


class ValidationMinOccurrenceError(ValidationError):
  
  def __init__(self, path, expected_schema, min_count):
    self.path = path
    self.expected_schema = expected_schema
    self.min_count = min_count

  def format(self, formatter):
    return formatter.format_min_occurrence_error(self)


class ValidationExactlyOccurrenceError(ValidationError):
  
  def __init__(self, path, expected_schema, exactly_count):
    self.path = path
    self.expected_schema = expected_schema
    self.exactly_count = exactly_count

  def format(self, formatter):
    return formatter.format_exactly_occurrence_error(self)


class ValidationMissingKeyError(ValidationError):

  def __init__(self, path):
    self.path = path

  def format(self, formatter):
    return formatter.format_missing_key_error(self)


class ValidationExtraKeyError(ValidationError):

  def __init__(self, path, extra_key):
    self.path = path
    self.extra_key = extra_key

  def format(self, formatter):
    return formatter.format_extra_key_error(self)


class ValidationSchemaMismatchError(ValidationError):

  def __init__(self, path, actual_val, options):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.options = options

  def format(self, formatter):
    return formatter.format_schema_mismatch_error(self)


class ValidationSingleSchemaMismatchError(ValidationError):

  def __init__(self, path, actual_val, options):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.options = options

  def format(self, formatter):
    return formatter.format_single_schema_mismatch_error(self)


class ValidationEnumerationError(ValidationError):

  def __init__(self, path, actual_val, enumerators):
    self.path = path
    self.actual_val = actual_val
    self.actual_type = self._get_type_as_string(actual_val)
    self.enumerators = enumerators

  def format(self, formatter):
    return formatter.format_enumeration_error(self)
