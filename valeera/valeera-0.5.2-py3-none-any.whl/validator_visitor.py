import district42.json_schema
from .errors import *


class ValidatorVisitor(district42.json_schema.AbstractVisitor):

  def __is_type_valid(self, actual_val, valid_types, is_nullable):
    if type(actual_val) in valid_types: return True
    if is_nullable and actual_val is None: return True
    return False

  def __is_value_valid(self, actual_val, expected_val, is_nullable):
    if is_nullable and actual_val is None: return True
    return actual_val == expected_val

  def __is_value_allowed(self, actual_val, enumerators, is_nullable):
    if any(type(x) == type(actual_val) and x == actual_val for x in enumerators): return True
    if is_nullable and actual_val is None: return True
    return False

  def __get_pattern(self, schema):
    if 'pattern' in schema._params:
      return schema._params['pattern']

    if 'numeric' in schema._params:
      return r'^[0-9]*$'
    
    if 'lowercase' in schema._params:
      pattern = 'a-z'
    elif 'uppercase' in schema._params:
      pattern = 'A-Z'
    else:
      pattern = 'a-zA-Z'

    if 'alphabetic' in schema._params:
      return r'^[{}]*$'.format(pattern)

    if 'alpha_num' in schema._params:
      return r'^[{}]*$'.format(pattern + '0-9')

    return r'^.*$'

  def __is_pattern_match(self, actual_val, pattern):
    import re
    return re.compile(pattern).match(actual_val)

  def __is_length_match(self, actual_val, expected_length, comparator):
    return getattr(len(actual_val), comparator)(expected_length)

  def __count_occurrences(self, schema, array, pointer):
    count = 0
    for index, item in enumerate(array):
      errors = schema.accept(self, pointer.move(index))
      if len(errors) == 0:
        count += 1
    return count

  def __is_undefined(self, schema):
    return type(schema) is district42.json_schema.types.Undefined

  def __is_required(self, schema):
    return 'required' not in schema._params or schema._params['required']
  
  def visit_null(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    if actual_val is not None:
      return [ValidationTypeError(path, actual_val, 'null')]

    return []

  def visit_boolean(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []

    is_type_valid = self.__is_type_valid(actual_val, schema._valuable_types, is_nullable)
    if not is_type_valid:
      expected_types = ['boolean', 'null'] if is_nullable else 'boolean'
      return [ValidationTypeError(path, actual_val, expected_types)]

    if 'value' in schema._params:
      expected_val = schema._params['value']
      is_value_valid = self.__is_value_valid(actual_val, expected_val, is_nullable)
      if not is_value_valid:
        return [ValidationValueError(path, actual_val, expected_val)]

    return []

  def visit_number(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []

    is_type_valid = self.__is_type_valid(actual_val, schema._valuable_types, is_nullable)
    if not is_type_valid:
      expected_types = ['number', 'null'] if is_nullable else 'number'
      return [ValidationTypeError(path, actual_val, expected_types)]

    if 'value' in schema._params:
      expected_val = schema._params['value']
      is_value_valid = self.__is_value_valid(actual_val, expected_val, is_nullable)
      if not is_value_valid:
        return [ValidationValueError(path, actual_val, expected_val)]

    errors = []
    if 'min_value' in schema._params:
      if actual_val < schema._params['min_value']:
        errors += [ValidationMinValueError(path, actual_val, schema._params['min_value'])]

    if 'max_value' in schema._params:
      if actual_val > schema._params['max_value']:
        errors += [ValidationMaxValueError(path, actual_val, schema._params['max_value'])]

    if ('multiple' in schema._params) and (actual_val % schema._params['multiple'] != 0):
      errors += [ValidationRemainderError(path, actual_val, schema._params['multiple'])]

    return errors

  def visit_integer(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []

    is_type_valid = self.__is_type_valid(actual_val, schema._valuable_types, is_nullable)
    if not is_type_valid:
      expected_types = ['integer', 'null'] if is_nullable else 'integer'
      return [ValidationTypeError(path, actual_val, expected_types)]

    if 'value' in schema._params:
      expected_val = schema._params['value']
      is_value_valid = self.__is_value_valid(actual_val, expected_val, is_nullable)
      if not is_value_valid:
        return [ValidationValueError(path, actual_val, expected_val)]

    errors = []
    if 'min_value' in schema._params:
      if actual_val < schema._params['min_value']:
        errors += [ValidationMinValueError(path, actual_val, schema._params['min_value'])]

    if 'max_value' in schema._params:
      if actual_val > schema._params['max_value']:
        errors += [ValidationMaxValueError(path, actual_val, schema._params['max_value'])]

    if ('multiple' in schema._params) and (actual_val % schema._params['multiple'] != 0):
      errors += [ValidationRemainderError(path, actual_val, schema._params['multiple'])]

    return errors

  def visit_float(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []

    is_type_valid = self.__is_type_valid(actual_val, schema._valuable_types, is_nullable)
    if not is_type_valid:
      expected_types = ['float', 'null'] if is_nullable else 'float'
      return [ValidationTypeError(path, actual_val, expected_types)]

    if 'value' in schema._params:
      expected_val = schema._params['value']
      is_value_valid = self.__is_value_valid(actual_val, expected_val, is_nullable)
      if not is_value_valid:
        return [ValidationValueError(path, actual_val, expected_val)]

    errors = []
    if 'min_value' in schema._params:
      if actual_val < schema._params['min_value']:
        errors += [ValidationMinValueError(path, actual_val, schema._params['min_value'])]

    if 'max_value' in schema._params:
      if actual_val > schema._params['max_value']:
        errors += [ValidationMaxValueError(path, actual_val, schema._params['max_value'])]

    return errors

  def visit_string(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []

    is_type_valid = self.__is_type_valid(actual_val, schema._valuable_types, is_nullable)
    if not is_type_valid:
      expected_types = ['string', 'null'] if is_nullable else 'string'
      return [ValidationTypeError(path, actual_val, expected_types)]

    if 'value' in schema._params:
      expected_val = schema._params['value']
      is_value_valid = self.__is_value_valid(actual_val, expected_val, is_nullable)
      if not is_value_valid:
        return [ValidationValueError(path, actual_val, expected_val)]

    pattern = self.__get_pattern(schema)
    is_pattern_match = self.__is_pattern_match(actual_val, pattern)
    if not is_pattern_match:
      return [ValidationPatternMismatchError(path, actual_val, pattern)]

    if 'length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['length'], '__eq__'):
        return [ValidationLengthError(path, actual_val, schema._params['length'])]

    if 'min_length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['min_length'], '__ge__'):
        return [ValidationMinLengthError(path, actual_val, schema._params['min_length'])]

    if 'max_length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['max_length'], '__le__'):
        return [ValidationMaxLengthError(path, actual_val, schema._params['max_length'])]

    return []

  def visit_array(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []

    valid_types = [list]
    is_type_valid = self.__is_type_valid(actual_val, valid_types, is_nullable)
    if not is_type_valid:
      expected_types = ['array', 'null'] if is_nullable else 'array'
      return [ValidationTypeError(path, actual_val, expected_types)]

    errors = []
    if 'items' in schema._params:
      for index, item in enumerate(schema._params['items']):
        new_pointer = pointer.move(index)
        try:
          errors += item.accept(self, new_pointer)
        except IndexError:
          errors.append(ValidationIndexError(new_pointer.path()))

      expected_length = len(schema._params['items'])
      if not self.__is_length_match(actual_val, expected_length, '__le__'):
        errors.append(ValidationLengthError(path, actual_val, expected_length))
    elif 'contains' in schema._params:
      count = self.__count_occurrences(schema._params['contains'], actual_val, pointer)
      if count == 0:
        errors.append(ValidationMinOccurrenceError(path, schema._params['contains'], 1))
    elif 'contains_one' in schema._params:
      count = self.__count_occurrences(schema._params['contains_one'], actual_val, pointer)
      if count != 1:
        errors.append(ValidationExactlyOccurrenceError(path, schema._params['contains_one'], 1))
    elif 'contains_many' in schema._params:
      count = self.__count_occurrences(schema._params['contains_many'], actual_val, pointer)
      if count < 2:
        errors.append(ValidationMinOccurrenceError(path, schema._params['contains_many'], 2))

    if 'length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['length'], '__eq__'):
        errors.append(ValidationLengthError(path, actual_val, schema._params['length']))

    if 'min_length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['min_length'], '__ge__'):
        errors.append(ValidationMinLengthError(path, actual_val, schema._params['min_length']))

    if 'max_length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['max_length'], '__le__'):
        errors.append(ValidationMaxLengthError(path, actual_val, schema._params['max_length']))

    return errors

  def visit_array_of(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []

    valid_types = [list]
    is_type_valid = self.__is_type_valid(actual_val, valid_types, is_nullable)
    if not is_type_valid:
      expected_types = ['array', 'null'] if is_nullable else 'array'
      return [ValidationTypeError(path, actual_val, expected_types)]

    errors = []
    for index, item in enumerate(actual_val):
      errors += schema._params['items_schema'].accept(self, pointer.move(index))

    if 'length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['length'], '__eq__'):
        errors.append(ValidationLengthError(path, actual_val, schema._params['length']))

    if 'min_length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['min_length'], '__ge__'):
        errors.append(ValidationMinLengthError(path, actual_val, schema._params['min_length']))

    if 'max_length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['max_length'], '__le__'):
        errors.append(ValidationMaxLengthError(path, actual_val, schema._params['max_length']))

    return errors

  def visit_object(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []

    valid_types = [dict]
    is_type_valid = self.__is_type_valid(actual_val, valid_types, is_nullable)
    if not is_type_valid:
      expected_types = ['object', 'null'] if is_nullable else 'object'
      return [ValidationTypeError(path, actual_val, expected_types)]
 
    errors = []
    for key, item_schema in schema._params['keys'].items():
      new_pointer = pointer.move(key)
      if self.__is_undefined(item_schema):
        if new_pointer.has_value():
          errors += [ValidationExtraKeyError(new_pointer.path(), key)]
      else:
        try:
          errors += item_schema.accept(self, new_pointer)
        except KeyError:
          if self.__is_required(item_schema):
            errors += [ValidationMissingKeyError(new_pointer.path())]

    if 'length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['length'], '__eq__'):
        errors += [ValidationLengthError(path, actual_val, schema._params['length'])]

    if 'min_length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['min_length'], '__ge__'):
        errors += [ValidationMinLengthError(path, actual_val, schema._params['min_length'])]

    if 'max_length' in schema._params:
      if not self.__is_length_match(actual_val, schema._params['max_length'], '__le__'):
        errors += [ValidationMaxLengthError(path, actual_val, schema._params['max_length'])]

    return errors

  def visit_any(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params

    valid_types = [bool, int, float, str, list, dict]
    is_type_valid = self.__is_type_valid(actual_val, valid_types, is_nullable)
    if not is_type_valid:
      expected_types = ['boolean', 'number', 'string', 'array', 'object']
      if is_nullable: expected_types.append('null')
      return [ValidationTypeError(path, actual_val, expected_types)]

    return []

  def visit_any_of(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []

    for option in schema._params['options']:
      option_errors = option.accept(self, pointer)
      if len(option_errors) == 0:
        return []
    
    return [ValidationSchemaMismatchError(path, actual_val, schema._params['options'])]

  def visit_one_of(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []
    
    count = 0
    for option in schema._params['options']:
      option_errors = option.accept(self, pointer)
      if len(option_errors) == 0:
        count += 1

    if count == 1:
      return []

    return [ValidationSingleSchemaMismatchError(path, actual_val, schema._params['options'])]

  def visit_enum(self, schema, pointer):
    path, actual_val = pointer.path(), pointer.value()

    is_nullable = 'nullable' in schema._params
    if is_nullable and actual_val is None:
      return []

    enumerators = schema._params['enumerators']
    is_value_allowed = self.__is_value_allowed(actual_val, enumerators, is_nullable)
    if not is_value_allowed:
      return [ValidationEnumerationError(path, actual_val, enumerators)]

    return []
