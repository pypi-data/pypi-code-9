from django import forms
from django.forms.models import modelform_factory
from django.test import TestCase

from ..forms import Form1, Form1Dedup, Form2
from ..models import Example, Example2
from smartforms import CompositeForm, CompositeModelForm


class ClassInitTest(TestCase):
    def test_empty_init(self):
        """
        Test empty initialization: all subforms are reprezented in the list, and none of them is bounded.
        """
        form_classes = [Form1, Form2]
        form = CompositeForm(form_classes=form_classes)
        for i in range(0, len(form._subforms)):
            act = form._subforms[i]
            self.assertIsInstance(act, form_classes[i])
            self.assertEquals(act.is_bound, False)
        self.assertEquals(form.is_bound, False)

    def test_post_init(self):
        """
        Passing POST data to parent form -> the form is bounded (and all subforms to).
        """
        post = {'data': 'example'}
        form_classes = [Form1, Form2]
        form = CompositeForm(data=post, form_classes=form_classes)
        self.assertEquals(form.is_bound, True)

    def test_fields_represented(self):
        """
        Subform fields are represented in CompositeForm
        """
        form_classes = [Form1, Form2]
        form = CompositeForm(form_classes=form_classes)
        fields = form.fields

        fields2 = Form1().fields
        fields2.update(Form2().fields)

        self.assertEquals(fields.keys(), fields2.keys())

    def test_deduplicate_fields(self):
        """
        Multiple form fields are deduplicated, and last defined is used.
        """
        class DedupForm(forms.Form):
            field1 = forms.CharField()
            field1 = forms.IntegerField()

        fields1 = DedupForm().fields

        form = CompositeForm(form_classes=[Form1, Form1Dedup])
        fields2 = form.fields

        self.assertEquals(fields1.keys(), fields2.keys())
        self.assertEquals(len(fields2.keys()), 1)


class InstanceInitTest(TestCase):
    def test_both_error(self):
        form_instances = [Form1(), Form2()]
        form_classes = [Form1, Form2]

        self.assertRaises(AttributeError, lambda: CompositeForm(form_instances=form_instances, form_classes=form_classes))

    def test_init_with_instances(self):
        post_data = {'field1': 'example', 'field2': 1}
        form1 = Form1(data=post_data)
        form2 = Form2(data=post_data)

        form = CompositeForm(form_instances=[form1, form2])
        self.assertEquals(len(form._subforms), 2)
        self.assertEquals(form.is_valid(), True)


class ModelInitTest(TestCase):
    def test_init_modelforms(self):
        mform1 = modelform_factory(model=Example, fields=['a', 'b'])()
        mform2 = modelform_factory(model=Example2, exclude=['d'])()

        instances = [mform1, Form1()]
        self.assertRaises(ValueError, lambda: CompositeModelForm(form_instances=instances))

        instances = [mform1, mform2]
        form = CompositeModelForm(form_instances=instances)
        self.assertIsInstance(form, CompositeModelForm)
        self.assertTrue(hasattr(form, 'save'))

    def test_save_modelform(self):
        mform1 = modelform_factory(model=Example, fields=['a', 'b'])({'a': 'a', 'b': 2})
        mform2 = modelform_factory(model=Example2, exclude=['d'])({'c': 'c'})

        instances = [mform1, mform2]
        form = CompositeModelForm(form_instances=instances)
        form.save()

        self.assertEquals(Example.objects.filter(a='a', b=2).count(), 1)
        self.assertEquals(Example2.objects.filter(c='c').count(), 1)

    def test_save_rollback(self):
        mform1 = modelform_factory(model=Example, fields=['a', 'b'])({'a': 'a'})
        mform2 = modelform_factory(model=Example2, exclude=['d'])({'c': 'c'})

        instances = [mform1, mform2]
        form = CompositeModelForm(form_instances=instances)

        self.assertRaises(ValueError, lambda: form.save())
        self.assertEquals(Example.objects.count(), 0)
        self.assertEquals(Example2.objects.count(), 0)