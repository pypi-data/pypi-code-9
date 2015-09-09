import json

from restify.serializers import ModelSerializer

from django import forms
from django.test import TestCase


class Frm(forms.Form):
    first = forms.CharField()
    second = forms.ChoiceField(choices=[(1, 1), (2, 2)])


class BaseSerializerTest(TestCase):
    def setUp(self):
        self.serializer = ModelSerializer()

    def test_form_serialize(self):
        form = Frm({'first': None, 'second': 'asdf'})
        simple = self.serializer.flatten(form)
        self.assertIsInstance(simple, {}.__class__)
        self.assertEqual(set(simple.keys()), set(['first', 'second']))
