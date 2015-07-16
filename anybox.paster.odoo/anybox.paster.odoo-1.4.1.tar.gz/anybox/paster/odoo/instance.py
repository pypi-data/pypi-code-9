# -*- coding: utf-8 -*-
from paste.script.templates import Template
from datetime import date
import shutil
import os

VERSION_FROM_GITHUB = "git http://github.com/anybox/odoo.git odoo 8.0 depth=1"
VERSION_FROM_NIGHTLY = "nightly 8.0 latest"


class Instance(Template):
    summary = ("Template for creating an Odoo Instance using buildout")
    required_templates = []
    _template_dir = 'templates/instance'
    use_cheetah = True

    def pre(self, command, output_dir, vars):
        vars['year'] = str(date.today().year)

        # common questions
        loopvars = [
            ('author', 'author name', 'Anybox'),
            ('author_email', 'author email', ''),
            ('author_website', 'author website', 'http://anybox.fr'),
            ('description', 'small description', ''),
        ]
        required = [
            'author',
            'description',
        ]
        while loopvars:
            var, question, default = loopvars[0]
            question = "Please enter the " + question + ' :'
            answer = command.challenge(question, default, True)
            if var not in required or answer != '':
                vars[var] = answer
                loopvars.pop(0)

        # git or nightly?
        answer = ''
        while answer.lower().strip() not in ('n', 'g'):
            question = "Use a [n]ightly release or [g]ithub development branches? n/g:"
            answer = command.challenge(question, '', True)
        if answer == 'g':
            vars['version_origin'] = VERSION_FROM_GITHUB
        elif answer == 'n':
            vars['version_origin'] = VERSION_FROM_NIGHTLY

    def post(self, command, output_dir, vars):

        print('\nYour instance is ready to build in the "%s" directory. '
              'Now you can run:\npython bootstrap.py\n./bin/buildout'
              '  # or: ./bin/buildout -c buildout.dev.cfg ' % vars['project'])
