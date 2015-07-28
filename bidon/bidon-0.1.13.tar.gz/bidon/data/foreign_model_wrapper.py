"""Contains the ForeignModelWrapper class."""
from . import ModelBase
from bidon.util import xml


class ForeignModelWrapper(ModelBase):
  """Provides a simple way to map incoming data into a model base."""
  timestamps = None
  table_name = None
  primary_key_name = None
  primary_key_is_auth = False
  mapping_format = "raw"
  mapping = dict()
  submodels = dict()

  @classmethod
  def apply_mapping(cls, from_dict, *, mapping=None):
    """Apply the class' mappings to a dictionary to create a new dictionary that can be used to
    initialize a new class instance.
    """
    if mapping is None:
      mapping = cls.mapping

    result = dict()
    for to_key, (from_key, transform) in mapping.items():
      value = from_dict.get(from_key)
      if value is not None and transform is not None:
        try:
          value = transform(value)
        except Exception as ex:
          raise Exception("Error with {0}->{1} conversion value {2}.\nAll data: {3}".format(
            from_key, to_key, value, from_dict)) from ex
      result[to_key] = value
    return result

  @classmethod
  def create(cls, from_item, *, mapping_format=None, mapping=None):
    """Passes from_item to apply_mapping and uses the result to construct a new class instance."""
    if mapping_format is None:
      mapping_format = cls.mapping_format

    if mapping_format == "raw":
      model = cls(cls.apply_mapping(from_item, mapping=mapping))
    elif mapping_format == "xml":
      model = cls(xml.transform(from_item, mapping or cls.mapping))
    else:
      raise ValueError("mapping_format must be one of {'raw', 'xml'}")

    for key, submodel in cls.submodels.items():
      value = getattr(model, key)

      if isinstance(value, list):
        new_value = [submodel(lv) for lv in value]
      else:
        new_value = submodel(value)

      setattr(model, key, new_value)

    return model

  @classmethod
  def map(cls, iterables, *, mapping_format=None, mapping=None):
    for idx, iterable in enumerate(iterables):
      try:
        yield cls.create(iterable, mapping_format=mapping_format, mapping=mapping)
      except Exception as ex:
        raise Exception("An error occurred with item {0}".format(idx)) from ex
