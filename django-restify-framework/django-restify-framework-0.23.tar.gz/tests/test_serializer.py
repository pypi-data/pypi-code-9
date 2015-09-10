import datetime
import random

from django import forms
from django.test import TestCase

from .paginator import page
from restify.serializers import ModelSerializer, DjangoSerializer


class Frm(forms.Form):
    first = forms.CharField()
    second = forms.ChoiceField(choices=[(1, 1), (2, 2)])


class Structure(object):
    value1 = random.randint(1, 100)
    value2 = datetime.datetime.now()
    value3 = Frm({'first': 'example', 'second': 1})

    def flatten(self):
        retval = {
            'value1': self.value1,
            'value2': self.value2.strftime('%Y-%m-%d %H:%M')
        }
        if self.value3.is_valid():
            retval['frm'] = {
                'first': self.value3.cleaned_data['first'],
                'second': self.value3.cleaned_data['second']
            }

        return retval


class BaseSerializerTest(TestCase):
    def setUp(self):
        self.serializer = ModelSerializer()

    def test_form_serialize(self):
        form = Frm({'first': None, 'second': 'asdf'})
        simple = self.serializer.flatten(form)
        self.assertIsInstance(simple, {}.__class__)
        self.assertEqual(set(simple.keys()), set(['first', 'second']))

    def test_serialize_with_flatten(self):
        obj = Structure()
        simple = self.serializer.flatten(obj)

        self.assertSequenceEqual(simple, obj.flatten())


################################# DjangoSearializer

class DjangoSerializerTest(TestCase):
    def setUp(self):
        self.serializer = DjangoSerializer()

    def test_paginator_serializer(self):
        serialized = {
            "current": page.number,
            "list": [{'key': 1, 'value': 1}, {'key': 2, 'value': 2}, None], # previous, current, next (if we have)
            "num_pages": page.paginator.num_pages
        }

        simple = self.serializer.flatten(page)

        self.assertEqual(simple, serialized)