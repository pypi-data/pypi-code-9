from collections import OrderedDict

from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer


def modelserializer_factory(mdl, fields=None, **kwargss):
    """ Generalized serializer factory to increase DRYness of code.

    :param mdl: The model for the ModelSerializer
    :param fields: The fields that should be exclusively present on the serializer
    :param kwargss: Optional additional field specifications
    :return: An awesome ModelSerializer
    """

    def _get_declared_fields(attrs):
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, Field)]
        fields.sort(key=lambda x: x[1]._creation_counter)
        return OrderedDict(fields)

    # Create an object that will look like a base serializer
    class Base(object):
        pass

    Base._declared_fields = _get_declared_fields(kwargss)

    class MySerializer(Base, ModelSerializer):
        class Meta:
            model = mdl

        if fields:
            setattr(Meta, "fields", fields)

    return MySerializer
