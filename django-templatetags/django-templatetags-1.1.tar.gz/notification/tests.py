# coding: utf-8
from django.test import TestCase

from django.template import Context
from django.template import Template
# Create your tests here.


class TemplateTagTest(TestCase):
    def setUp(self):
        self.template = Template('{% load notify %} {% render_notification %}')

    def test_templatetag_inclusion(self):
        rendered = self.template.render(Context())
        self.assertIn('am a notification', rendered)


class FilterTest(TestCase):
    def setUp(self):
        self.template = Template('{% load notify %}' +
                ' {{ "Hello %s, How are you?"|format_hello:"Élysson MR" }}')

    def test_filter(self):
        rendered = self.template.render(Context())
        self.assertIn(u'Élysson MR', rendered)

