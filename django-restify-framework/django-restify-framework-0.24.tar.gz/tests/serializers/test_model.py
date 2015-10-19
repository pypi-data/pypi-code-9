from django.db import models
from django.test import TestCase

from restify.serializers import ModelSerializer


class Related(models.Model):
    first = models.CharField(max_length=10, default='first')


class Model1(models.Model):
    a = models.CharField(max_length=100)
    b = models.PositiveIntegerField(default=10)
    c = models.ForeignKey(Related, related_name='relmodel')


class ModelSerializerTestCase(TestCase):
    def setUp(self):
        obj = Related()
        obj.save()

        Model1(a='example', c=obj).save()
        self.serializer = ModelSerializer(serialize_related_fields=False)

    def test_model_serializer_without_relations(self):
        obj = Model1.objects.first()
        flatten = self.serializer.flatten(obj)

        serialized = {
            'id': obj.pk,
            'a': obj.a,
            'b': obj.b
        }

        self.assertEqual(flatten, serialized)

    def test_model_serializer_with_relations(self):
        obj = Model1.objects.first()
        self.serializer._serialize_related_fields = True
        flatten = self.serializer.flatten(obj)

        serialized = {
            'id': obj.pk,
            'a': obj.a,
            'b': obj.b,
            'c': obj.c.pk
        }

        self.assertEqual(flatten, serialized)
