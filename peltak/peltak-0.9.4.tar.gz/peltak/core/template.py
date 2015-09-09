#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re
import os.path
from collections import OrderedDict


class Template(object):
    """ A simple implementation of a text template for merge requests.

    The class has 2 properties that are filled:

    :context:R
    """
    def __init__(self, content=None):
        self.content = content

    @classmethod
    def load_from_file(self, path):
        """ Load the template from file.

        During the load, the template will be preprocessed and ``context`` and
        ``checklist`` will be extracted.
        """
        if not os.path.exists(path):
            return None

        with open(path) as fp:
            content = fp.read()
            return Template(content)

    @property
    def content(self):
        """ Return the template content. """
        return self._content

    @content.setter
    def content(self, value):
        """ Set template content.

        This will process the template and extract placeholders and the
        checklist.
        """
        self._content = value
        self.context = {}
        if value is not None:
            self.context = self._extract_context(value)
            self.checklist = self._extract_checklist(value)

    def _extract_context(self, text):
        ret = OrderedDict()
        if text is not None:
            for m in re.finditer(r'\$\{(.*?)\}', text):
                name = m.group(1)
                if name not in ret:
                    ret[name] = ''
        return ret

    def _extract_checklist(self, text):
        ret = OrderedDict()
        if text is not None:
            for m in re.finditer(r'^\- \[ \] (.*)$', text, flags=re.M):
                question = m.group(1)
                if question not in ret:
                    ret[question] = None
        return ret

    def fill(self, src):
        """ Fill in the context and checklist from a given dict like object."""
        for key in self.context:
            if key in src:
                self.context[key] = src[key]

        for key in self.checklist:
            if key in src:
                self.checklist[key] = src[key]

    def render(self):
        """ Render the template to string.

        This will replace all the palceholders and the update the checklist
        according to values stored in ``self.checklist`` and ``self.context``.
        """
        out = self.content

        # Fill in the context
        for name, value in self.context.items():
            pttrn = r'\$\{{{}\}}'.format(re.escape(name))
            out = re.sub(pttrn, value or '<MISSING>', out)

        # Fill in the checklist
        for todo, complete in self.checklist.items():
            pttrn = r'^- \[ \] {}$'.format(re.escape(todo))
            item = '- [{}] {}'.format('x' if complete else ' ', todo)
            out = re.sub(pttrn, item, out, flags=re.M)

        return out

