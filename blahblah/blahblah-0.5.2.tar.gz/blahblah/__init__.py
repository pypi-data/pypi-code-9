from .faker import Faker


def fake(schema, *args):
  return schema.accept(Faker(), *args)
