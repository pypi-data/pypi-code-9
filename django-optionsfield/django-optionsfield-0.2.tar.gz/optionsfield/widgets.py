#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"
import re

from django.forms import widgets
from pkg_resources import resource_string

from .options import Options

TEMPLATE_NAME = 'templates/admin/optionsfield/widget.html'


class OptionsWidget(widgets.TextInput):

    def __init__(self, attrs=None):
        super(OptionsWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        # its here so its not accessed on package build time
        # - then django fails on not being configured
        from django.template import Template, Context
        # I manually open the file here so we dont need
        # to add this package to INSTALLED_APPS
        template = resource_string(__name__, TEMPLATE_NAME)
        template = Template(template)
        context = Context({'name': name, 'options': value})
        return template.render(context)

    def value_from_datadict(self, data, files, name):

        opt = {}

        # collect all options keys and values and pair them
        for key in data:
            match = re.match(r'^{}_(key|val)_(\d+)$'.format(name), key)
            if match:
                value = data[key]
                t, i = match.groups()
                if i not in opt:
                    opt[i] = {}
                opt[i][t] = value

        options = Options()
        for i, option in sorted(opt.items()):
            try:
                options[option['key']] = option['val']
            except KeyError:
                # incomplete, sorry
                pass

        return options

    def _format_value(self, value):
        if value:
            return value.to_string()
