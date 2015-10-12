from copy import deepcopy
import district42.json_schema


class Substitutor(district42.json_schema.AbstractVisitor):

  def __visit_valuable(self, schema, value):
    clone = deepcopy(schema)
    clone._params['value'] = value
    return clone

  def __determine_type(self, value):
    value_type = type(value)
    if value_type is bool:
      return district42.json_schema.boolean
    elif value_type is int:
      return district42.json_schema.integer
    elif value_type is float:
      return district42.json_schema.float
    elif value_type is str:
      return district42.json_schema.string
    elif value_type is list:
      return district42.json_schema.array
    elif value_type is dict:
      return district42.json_schema.object
    else:
      return district42.json_schema.null

  def __is_required(self, schema):
    return 'required' not in schema._params or schema._params['required']

  def __is_undefined(self, schema):
    return type(schema) is district42.json_schema.types.Undefined

  def visit_null(self, schema, *args):
    return deepcopy(schema)

  def visit_boolean(self, schema, value):
    return self.__visit_valuable(schema, value)

  def visit_number(self, schema, value):
    return self.__visit_valuable(schema, value)

  def visit_integer(self, schema, value):
    return self.__visit_valuable(schema, value)

  def visit_float(self, schema, value):
    return self.__visit_valuable(schema, value)

  def visit_string(self, schema, value):
    return self.__visit_valuable(schema, value)

  def visit_array(self, schema, items):
    array_items = []
    for item in items:
      array_items += [self.__determine_type(item) % item]
    return district42.json_schema.array(array_items)

  def visit_array_of(self, schema, items):
    return self.visit_array(schema, items)

  def visit_object(self, schema, keys):
    clone = deepcopy(schema)
    for key in clone._params['keys']:
      if key in keys and not self.__is_undefined(clone._params['keys'][key]):
        if not self.__is_required(clone._params['keys'][key]):
          clone._params['keys'][key]._params['required'] = True
        clone._params['keys'][key] %= keys[key]
    return clone

  def visit_any(self, schema, value):
    return self.__determine_type(value) % value

  def visit_any_of(self, schema, value):
    return self.__determine_type(value) % value

  def visit_one_of(self, schema, value):
    return self.__determine_type(value) % value

  def visit_enum(self, schema, value):
    return self.__determine_type(value) % value

  def visit_undefined(self, schema):
    raise NotImplementedError()
