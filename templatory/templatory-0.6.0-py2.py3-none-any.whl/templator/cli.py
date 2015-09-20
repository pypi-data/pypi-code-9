# -*- coding: UTF-8 -*-

"""
CLI functions.

"""

from __future__ import absolute_import
from __future__ import unicode_literals


import argparse

from . import __VERSION__
from .templates import get_supported_templates


class AddToDict(argparse.Action):

  """
  Custom action for the argument parser:

  It takes two *values* (a key and a value) and stores it in the dictionary
  bound to the argument (`self.dest`).

  """

  def __call__(self, parser, namespace, values, option_string=None):
    key, value = values
    getattr(namespace, self.dest)[key] = value


def get_argument_parser():
  """
  Returns an argument parser.

  """
  templates = get_supported_templates()
  option_string = (
    '[--extra <KEY> <VALUE>]… [--data <FILE>…] '
    '[--content <FILE>…] [--css <FILE>…] [--js <FILE>…]'
  )
  ap = argparse.ArgumentParser(
    usage='templator {options} [<TEMPLATEFILE>]…'.format(
      options=option_string
    ),
    description='Builds a context and prints the rendered TEMPLATEs to `stdout`.'
  )
  # ARGUMENTS
  ap.add_argument(
    'templates', metavar='FILE', nargs='*',
    help="JINJA2 template(s) to use (default: simple HTML5 wrapper)"
  )
  # OPTIONS
  ap.add_argument('--version', action='version', version=__VERSION__)
  ap.add_argument(
    '-v', '--verbose', action='count',
    help="show additional output"
  )
  # INPUT
  g_in = ap.add_argument_group(
    'Input', (
      "Load data into the context. "
      "The content from datafiles is is available for the templates in their "
      "context — if you load a YAML file, that sets the value `foo`, it is is "
      "available as `context.foo`. "
      "You can load the contents of files into the context too, use "
      "`--content` for that. If only one file is given, it's contents are "
      "available directly under `context.content`, if more files are given, "
      "`context.content` is a dictionary, indexing the contents by filename."
    )
  )
  g_in.add_argument(
    '-e', '--extra', action=AddToDict, nargs=2, metavar='STRING',
    help="add `key value` pair to the context"
  )
  g_in.add_argument(
    '-d', '--data', metavar='FILE', nargs='+', dest='data_files',
    help="add data from FILE (JSON / YAML) to the context"
  )
  g_in.add_argument(
    '-c', '--content', metavar='FILE', nargs='+', dest='content_files',
    help="`content` for the context — MD or RST files get rendered before usage"
  )
  # OUTPUT
  g_out = ap.add_argument_group(
    'Output',
    (
      "Pass the context to the template(s). "
      "You can either supply template files as positional arguments, name one "
      "of the default templates to be use or supply a template as string — "
      "but you can't mix those options. "
      "If no template is set, a default HTML 5 template is used."
    )
  )
  meg_tpl = g_out.add_mutually_exclusive_group()
  meg_tpl.add_argument(
    '-t', '--template-name', metavar='STRING', choices=templates.keys(),
    help="choose template to use"
  )
  meg_tpl.add_argument(
    '-T', '--template-string', metavar='STRING',
    help="use template STRING"
  )
  g_out.add_argument(
    '-m', '--merger', metavar='STRING',
    help="join output of all templates with this STRING"
  )
  # HTML
  g_html = ap.add_argument_group(
    'HTML', "Special options for HTML templates."
  )
  g_html.add_argument(
    '-C', '--css', metavar='FILE', nargs='+', dest='css_files',
    help="include the content of each FILE in it's own `style` tag"
  )
  g_html.add_argument(
    '-J', '--javascript', metavar='FILE', nargs='+', dest='js_files',
    help="include the content of each FILE in it's own `script` tag"
  )
  g_html.add_argument(
    '-M', '--minimize', action='store_true',
    help="minimize output"
  )
  # MODES
  g_mo = ap.add_argument_group(
    'Modes', "Do other things than render templates."
  )
  meg_mo = g_mo.add_mutually_exclusive_group()
  meg_mo.add_argument(
    '--list-templates', action='store_true',
    help="lists all available templates and exit"
  )
  meg_mo.add_argument(
    '--list-variables', choices=templates.keys(),
    help="lists context variables for TEMPLATE and exit"
  )
  meg_mo.add_argument(
    '--show-context', action='store_true',
    help="show context and exit"
  )
  # set defaults
  ap.set_defaults(
    verbose=0,
    content_files=[],
    data_files=[],
    extra={},
    template_name=None,
    template_string='',
    template_files=[],
    merger='\n',
    css_files=[],
    js_files=[],
    minimize=False,
    show_context=False,
    list_templates=False,
    list_variables=False,
  )
  return ap
