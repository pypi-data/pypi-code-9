from district42.json_schema.types import SchemaType
from .faker import Faker
from .substitutor import Substitutor


def fake(schema, *args):
  return schema.accept(Faker(), *args)

SchemaType.__mod__ = lambda self, val: self.accept(Substitutor(), val)
