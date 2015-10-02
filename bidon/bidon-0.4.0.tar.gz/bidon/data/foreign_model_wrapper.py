"""Contains the ForeignModelWrapper class."""
from . import ModelBase
from bidon.util.transform import get_obj


class ForeignModelWrapper(ModelBase):
  timestamps = None
  table_name = None
  primary_key_name = None
  primary_key_is_auto = False
  transform_args = None

  @classmethod
  def create(cls, source, *, transform_args=None):
    if transform_args is None:
      transform_args = cls.transform_args

    return cls(get_obj(source, *transform_args))

  @classmethod
  def map(cls, sources, *, transform_args=None):
    for idx, source in enumerate(sources):
      try:
        yield cls.create(source, transform_args=transform_args)
      except Exception as ex:
        raise Exception("An error occurred with item {0}".format(idx)) from ex

