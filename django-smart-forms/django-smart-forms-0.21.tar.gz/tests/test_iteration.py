from django.test import TestCase
from django.forms.forms import BoundField

from .forms import Form1, Form2
from smartforms import CompositeForm


class FieldAccessTest(TestCase):
    def setUp(self):
        form_classes = [Form1, Form2]
        self.form = CompositeForm(form_classes=form_classes)

    def test_self_fields(self):
        self.assertEquals(list(self.form.fields.keys()), ['field1', 'field2'])

        ## field is not bounded
        field = self.form.fields['field2']
        self.assertRaises(AttributeError, lambda: field.form)

    def test_access_bounded_field(self):
        field = self.form['field2']
        self.assertEquals(field.form.__class__, Form2)

    def test_field_iteration(self):
        self.assertEquals(hasattr(self.form, '__iter__'), True)
        for field in self.form:
            self.assertIn(field.name, ['field1', 'field2'])