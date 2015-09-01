from django import forms
from django.db.models import Sum
from django.test import TestCase

from smartforms import FormSet, ModelFormSet

from .forms import Form1, ModelForm, Model


class FormSetTest(TestCase):
    def test_init(self):
        form = FormSet(form_class=Form1, repeat=2)

        self.assertEquals(form.is_bound, False)
        self.assertEquals(len(form._subforms), 2)

        for subform in form._subforms:
            self.assertIsInstance(subform, Form1)

        for i in range(0, len(form._subforms)):
            prefix = 'form{0}'.format(i)
            self.assertEquals(form._subforms[i].prefix, prefix)

    def test_post_init(self):
        post = {'data': 'example'}
        form = FormSet(data=post, form_class=Form1, repeat=3)
        self.assertEquals(form.is_bound, True)

    def test_iter_fields(self):
        form = FormSet(form_class=Form1, repeat=3)

        self.assertEquals(len(Form1().fields) * 3, len(form.fields))

        for field in form.fields.values():
            self.assertIn(field.label, ['field1', 'field2'])

    def test_field_ordering(self):
        form = FormSet(form_class=Form1, repeat=3)

        last_counter = 0
        for field in form:
            field_counter = int(field.form.prefix.split('-')[0].replace('form', ''))
            self.assertGreaterEqual(field_counter, last_counter)
            last_counter = field_counter

    def test_post(self):
        post = {'form0-field1': 'asdf', 'form0-field2': 2}
        form = FormSet(post, form_class=Form1, repeat=2)

        ## Form isn't valid...
        self.assertFalse(form.is_valid())

        ### because of the second form
        self.assertTrue(form._subforms[0].is_valid())

    def test_minimal_post(self):
        post = {'form0-field1': 'asdf', 'form0-field2': 2}
        form = FormSet(post, form_class=Form1, repeat=2, min_valid=1)

        self.assertTrue(form.is_valid())

    def test_custom_parameter(self):
        """
        All parameters are passed to subforms.
        """
        form = FormSet(form_class=Form1, repeat=2, custom_parameter='example', label_suffix='suff')

        for subform in form._subforms:
            self.assertEquals(subform.param1, 'example')
            self.assertEquals(subform.label_suffix, 'suff')

    def test_iterable(self):
        form = FormSet(form_class=Form1, repeat=2)
        for field in form:
            self.assertIsInstance(field, forms.forms.BoundField)


class ModelFormSetTest(TestCase):
    def test_init(self):
        ## Form class must be modelform
        self.assertRaises(ValueError, lambda: ModelFormSet(form_class=Form1, repeat=2))

        post = {'form0-field1': 1, 'form1-field1': 2}
        form = ModelFormSet(post, form_class=ModelForm, repeat=2)
        form.save()
        self.assertEquals(Model.objects.count(), 2)

    def test_init_instances(self):
        model = Model.objects.create(field1=4)

        post = {'form0-field1': 1}
        form = ModelFormSet(post, form_class=ModelForm, repeat=1, instances=[model])
        form.save()

        self.assertEquals(Model.objects.count(), 1)

    def test_init_queryset(self):
        post = {}
        for i in range(0, 5):
            _ = Model.objects.create(field1=i)
            post['form{0}-field1'.format(i)] = 0

        s = Model.objects.all().aggregate(Sum('field1'))['field1__sum']
        self.assertEquals(s, 10)

        form = ModelFormSet(post, form_class=ModelForm, repeat=5, instances=Model.objects.all())
        form.save()

        s = Model.objects.all().aggregate(Sum('field1'))['field1__sum']
        self.assertEquals(s, 0)

    def test_empty_forms(self):
        post = {'form0-field1': 7}
        form = ModelFormSet(post, form_class=ModelForm, repeat=5, min_valid=1, instances=Model.objects.all())

        self.assertTrue(form.is_valid())
        form.save()

        self.assertEquals(Model.objects.count(), 1)