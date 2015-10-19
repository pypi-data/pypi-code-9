import datetime
import random

from django.test import TestCase
from restify.serializers import BaseSerializer


class Structure(object):
    value1 = random.randint(1, 100)
    value2 = datetime.datetime.now()

    def flatten(self):
        retval = {
            'value1': self.value1,
            'value2': self.value2
        }

        return retval


class NoFlattenStructure(object):
    value1 = random.randint(1, 100)
    value2 = datetime.datetime.now()

    def __str__(self):
        return "%s %s" % (self.value1, self.value2)


class BaseSerializerTest(TestCase):
    def setUp(self):
        self.serializer = BaseSerializer()

    def test_serialize_with_flatten(self):
        obj = Structure()
        simple = self.serializer.flatten(obj)

        self.assertSequenceEqual(simple, obj.flatten())

    def test_serialize_no_flatten(self):
        obj = NoFlattenStructure()
        simple = self.serializer.flatten(obj)

        self.assertSequenceEqual(simple, str(obj))
