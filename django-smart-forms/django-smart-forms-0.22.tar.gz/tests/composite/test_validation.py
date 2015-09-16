from django.test import TestCase

from ..forms import Form1, Form2
from smartforms import CompositeForm


class ValidationTest(TestCase):
    def setUp(self):
        form_classes = [Form1, Form2]
        post_data = {'field1': 'asdf'}
        self.form = CompositeForm(post_data, form_classes=form_classes)

    def test_form_has_errors(self):
        self.assertEquals(self.form.is_valid(), False)
        self.assertEquals(list(self.form.errors.keys()), ['field2'])

    def test_form_errors_as_json(self):
        self.assertIsInstance(self.form.errors.as_json(), str)

    def test_form_valid(self):
        post_data = {'field1': 'asdf', 'field2': 'asdf'}
        form_classes = [Form1, Form2]
        form = CompositeForm(post_data, form_classes=form_classes)
        self.assertEquals(form.is_valid(), True)
