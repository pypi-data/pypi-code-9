from .abstract_formatter import AbstractFormatter
from .pointer import Pointer


class Formatter(AbstractFormatter):

  types_map = {
    'NoneType': 'null',
    'bool':     'boolean',
    'int':      'number',
    'float':    'number',
    'str':      'string',
    'list':     'array',
    'dict':     'object'
  }

  def __get_article(self, word):
    return 'an' if word[0].lower() in 'aeiou' else 'a'

  def __to_json_type(self, python_type):
    return self.types_map.get(python_type, python_type)

  def __get_length_error_message(self, path, actual_type, accuracy, expected_length):
    actual_type = self.__to_json_type(actual_type)

    message = actual_type.capitalize()
    if path != Pointer.root:
      message += ' ' + path

    if actual_type == 'string':
      element = 'symbol'
    elif actual_type == 'object':
      element = 'key'
    else:
      element = 'element'

    if expected_length != 1:
      element += 's'

    return message + ' must have {} {} {}'.format(accuracy, expected_length, element)

  def format_type_error(self, error):
    actual_type = self.__to_json_type(error.actual_type)
    
    message = 'Value'
    if error.path != Pointer.root:
      message += ' ' + error.path
    
    if len(error.expected_types) == 1:
      article = self.__get_article(error.expected_types[0])
      message += ' must be {} {}'.format(article, error.expected_types[0])
    elif len(error.expected_types) == 2:
      message += ' must be {} {} or {} {}'.format(
        self.__get_article(error.expected_types[0]),
        error.expected_types[0],
        self.__get_article(error.expected_types[1]),
        error.expected_types[1]
      )
    else:
      message += ' must be one of the types: ({})'.format(', '.join(error.expected_types))
    
    if actual_type == 'null':
      return message + ', {} given'.format(actual_type)
    
    return message + ', {} {} given'.format(actual_type, repr(error.actual_val))

  def format_value_error(self, error):
    actual_type = self.__to_json_type(error.actual_type)
   
    message = actual_type.capitalize() + ' value'
    if error.path != Pointer.root:
      message += ' ' + error.path
    
    return message + ' must be equal to {}, {} given'.format(repr(error.expected_val),
                                                             repr(error.actual_val))

  def format_min_value_error(self, error):
    actual_type = self.__to_json_type(error.actual_type)
   
    message = actual_type.capitalize() + ' value'
    if error.path != Pointer.root:
      message += ' ' + error.path

    return message + ' must be greater than or equal to {}, {} given'.format(error.min_value,
                                                                             error.actual_val)

  def format_max_value_error(self, error):
    actual_type = self.__to_json_type(error.actual_type)
   
    message = actual_type.capitalize() + ' value'
    if error.path != Pointer.root:
      message += ' ' + error.path

    return message + ' must be less than or equal to {}, {} given'.format(error.max_value,
                                                                          error.actual_val)

  def format_remainder_error(self, error):
    actual_type = self.__to_json_type(error.actual_type)
    
    message = actual_type.capitalize()
    if error.path != Pointer.root:
      message += ' ' + error.path

    return message + ' must be a multiple of {}, {} given'.format(error.divisor,
                                                                  error.actual_val)

  def format_pattern_mismatch_error(self, error):
    message = 'String'
    
    if error.path != Pointer.root:
      message += ' ' + error.path
    
    return message + ' must match pattern "{}", {} given'.format(error.pattern,
                                                                 repr(error.actual_val))

  def format_length_error(self, error):
    return self.__get_length_error_message(error.path, error.actual_type, 'exactly',
                                           error.length)

  def format_min_length_error(self, error):
    return self.__get_length_error_message(error.path, error.actual_type, 'at least',
                                           error.min_length)

  def format_max_length_error(self, error):
    return self.__get_length_error_message(error.path, error.actual_type, 'at most',
                                           error.max_length)

  def format_index_error(self, error):
    return 'Element {} does not exist'.format(error.path)

  def format_min_occurrence_error(self, error):
    message = 'Array'
    
    if error.path != Pointer.root:
      message += ' ' + error.path
    
    return message + ' must contain at least {} occurrence{} of {}'.format(
      error.min_count,
      '' if error.min_count == 1 else 's',
      error.expected_schema
    )

  def format_exactly_occurrence_error(self, error):
    message = 'Array'
    
    if error.path != Pointer.root:
      message += ' ' + error.path
    
    return message + ' must contain exactly {} occurrence{} of {}'.format(
      error.exactly_count,
      '' if error.exactly_count == 1 else 's',
      error.expected_schema
    )
  
  def format_missing_key_error(self, error):
    return 'Key {} does not exist'.format(error.path)

  def format_extra_key_error(self, error):
    message = 'Object'
    
    if error.path != Pointer.root:
      message += ' ' + error.path
    
    return message + ' contains extra key "{}"'.format(error.extra_key)

  def format_schema_mismatch_error(self, error):
    message = 'Value'
    
    if error.path != Pointer.root:
      message += ' ' + error.path
    
    options = ',\n'.join(map(str, error.options))
    return message + ' must match any of the schemas:\n{}'.format(options)

  def format_single_schema_mismatch_error(self, error):
    message = 'Value'
    
    if error.path != Pointer.root:
      message += ' ' + error.path
    
    options = ',\n'.join(map(str, error.options))
    return message + ' must match one of the schemas:\n{}'.format(options)

  def format_enumeration_error(self, error):
    actual_type = self.__to_json_type(error.actual_type)
   
    message = actual_type.capitalize() + ' value'
    if error.path != Pointer.root:
      message += ' ' + error.path
    
    enumerators = ', '.join(map(repr, error.enumerators))
    return message + ' must be one of the following: ({}), {} given'.format(
      enumerators,
      repr(error.actual_val)
    )
