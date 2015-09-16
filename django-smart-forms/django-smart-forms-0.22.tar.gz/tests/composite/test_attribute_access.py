from django.test import TestCase

from ..forms import Form1, Form2
from smartforms import CompositeForm


class AccessAttributeTest(TestCase):
    def test_access_is_bound(self):
        form_classes = [Form1, Form2]
        form = CompositeForm(form_classes=form_classes)

        self.assertEqual(form.is_bound, False)

        form.is_bound = True
        self.assertEqual(form.is_bound, True)
        for subform in form._subforms:
            self.assertEqual(form.is_bound, True)