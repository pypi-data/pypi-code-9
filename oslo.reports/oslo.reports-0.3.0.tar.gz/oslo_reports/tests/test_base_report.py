# Copyright 2013 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import collections as col
import re

from oslotest import base
import six

from oslo_reports.models import base as base_model
from oslo_reports import report


class BasicView(object):
    def __call__(self, model):
        res = ""
        for k in sorted(model.keys()):
            res += six.text_type(k) + ": " + six.text_type(model[k]) + ";"
        return res


def basic_generator():
    return base_model.ReportModel(data={'string': 'value', 'int': 1})


class TestBasicReport(base.BaseTestCase):
    def setUp(self):
        super(TestBasicReport, self).setUp()

        self.report = report.BasicReport()

    def test_add_section(self):
        self.report.add_section(BasicView(), basic_generator)
        self.assertEqual(len(self.report.sections), 1)

    def test_append_section(self):
        self.report.add_section(BasicView(), lambda: {'a': 1})
        self.report.add_section(BasicView(), basic_generator)

        self.assertEqual(len(self.report.sections), 2)
        self.assertEqual(self.report.sections[1].generator, basic_generator)

    def test_insert_section(self):
        self.report.add_section(BasicView(), lambda: {'a': 1})
        self.report.add_section(BasicView(), basic_generator, 0)

        self.assertEqual(len(self.report.sections), 2)
        self.assertEqual(self.report.sections[0].generator, basic_generator)

    def test_basic_render(self):
        self.report.add_section(BasicView(), basic_generator)
        self.assertEqual(self.report.run(), "int: 1;string: value;")


class TestBaseModel(base.BaseTestCase):
    def test_submodel_attached_view(self):
        class TmpView(object):
            def __call__(self, model):
                return '{len: ' + six.text_type(len(model.c)) + '}'

        def generate_model_with_submodel():
            base_m = basic_generator()
            tv = TmpView()
            base_m['submodel'] = base_model.ReportModel(data={'c': [1, 2, 3]},
                                                        attached_view=tv)
            return base_m

        self.assertEqual(BasicView()(generate_model_with_submodel()),
                         'int: 1;string: value;submodel: {len: 3};')

    def test_str_throws_error_with_no_attached_view(self):
        model = base_model.ReportModel(data={'c': [1, 2, 3]})

        # ugly code for python 2.6 compat, since python 2.6
        # does not have assertRaisesRegexp
        try:
            six.text_type(model)
        except Exception as e:
            err_str = 'Cannot stringify model: no attached view'
            self.assertEqual(six.text_type(e), err_str)
        else:
            self.assertTrue(False)

    def test_str_returns_string_with_attached_view(self):
        model = base_model.ReportModel(data={'a': 1, 'b': 2},
                                       attached_view=BasicView())

        self.assertEqual(six.text_type(model), 'a: 1;b: 2;')

    def test_model_repr(self):
        model1 = base_model.ReportModel(data={'a': 1, 'b': 2},
                                        attached_view=BasicView())

        model2 = base_model.ReportModel(data={'a': 1, 'b': 2})

        base_re = r"<Model [^ ]+\.[^ ]+ \{.+\} with "
        with_view_re = base_re + r"view [^ ]+\.[^ ]+>"
        without_view_re = base_re + r"no view>"

        self.assertTrue(re.match(with_view_re, repr(model1)))
        self.assertTrue(re.match(without_view_re, repr(model2)))

    def test_getattr(self):
        model = base_model.ReportModel(data={'a': 1})

        self.assertEqual(model.a, 1)

        self.assertRaises(AttributeError, getattr, model, 'b')

    def test_data_as_sequence_is_handled_properly(self):
        model = base_model.ReportModel(data=['a', 'b'])
        model.attached_view = BasicView()

        # if we don't handle lists properly, we'll get a TypeError here
        self.assertEqual('0: a;1: b;', six.text_type(model))

    def test_immutable_mappings_produce_mutable_models(self):
        class SomeImmutableMapping(col.Mapping):
            def __init__(self):
                self.data = {'a': 2, 'b': 4, 'c': 8}

            def __getitem__(self, key):
                return self.data[key]

            def __len__(self):
                return len(self.data)

            def __iter__(self):
                return iter(self.data)

        mp = SomeImmutableMapping()
        model = base_model.ReportModel(data=mp)
        model.attached_view = BasicView()

        self.assertEqual('a: 2;b: 4;c: 8;', six.text_type(model))

        model['d'] = 16

        self.assertEqual('a: 2;b: 4;c: 8;d: 16;', six.text_type(model))
        self.assertEqual({'a': 2, 'b': 4, 'c': 8}, mp.data)
