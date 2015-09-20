# -*- coding: UTF-8 -*-

"""
Takes a *context* and renders one or more Jinja *templates* with it.

You can build the context by manually setting keywords, loading data files or
giving content as markup files.

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import sys
import argparse

from corelib.templates import (
  get_context,
  render
)


__VERSION__ = '0.4.0'

__ALL__ = [
  'render_template'
]

KEYWORDS = {
  'title': 'string to use as TITLE for the HTML',
  'css': 'each element of the list will be put in a STYLE tag',
  'js': 'each element of the list will be put in a SCRIPT tag',
  'content': 'contents for the BODY tag'
}

HTML = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {%- if title %}
  <title>{{ title }}</title>
  {%- endif %}
  {%- for css_content in css %}
  <style>{{ css_content }}</style>
  {%- endfor %}
  {%- for js_content in js %}
  <script>{{ js_content }}</script>
  {%- endfor %}
</head>
<body>{{ content }}</body>
</html>"""


class AddToDict(argparse.Action):

  """
  Custom action for the argument parser:

  It takes two *values* (a key and a value) and stores it in the dictionary
  bound to the argument (`self.dest`).

  """

  def __call__(self, parser, namespace, values, option_string=None):
    key, value = values
    getattr(namespace, self.dest)[key] = value


def _get_argument_parser():
  """
  Returns an argument parser.

  """
  option_string = (
    '[--content <FILE>…] [--data <FILE>…] [--extra <KEY> <VALUE>]… '
    '[--css <FILE>…] [--js <FILE>…]'
  )
  ap = argparse.ArgumentParser(
    usage='templator {options} [<TEMPLATE>]…'.format(options=option_string),
    description='Builds a context and prints the render TEMPLATEs to `stdout`.'
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
  ap.add_argument(
    '--debug', const=2, dest='verbose', nargs='?',
    help="show context and exit"
  )
  ap.add_argument(
    '-l', '--list', action='store_true',
    help="lists all special context variables for the default template"
  )
  # INPUT
  g_in = ap.add_argument_group(
    'Input', "Load data into the context."
  )
  g_in.add_argument(
    '-c', '--content', metavar='FILE', nargs='+', dest='content_files',
    help="`content` for the context — MD or RST files get rendered before usage"
  )
  g_in.add_argument(
    '-d', '--data', metavar='FILE', nargs='+', dest='data_files',
    help="add data from FILE (JSON / YAML) to the context"
  )
  g_in.add_argument(
    '-e', '--extra', action=AddToDict, nargs=2, metavar='STRING',
    help="add `key value` pair to the context"
  )
  # OUTPUT
  g_out = ap.add_argument_group(
    'Output',
    (
      "Pass the context to the template(s). "
      "If no template is set, a default HTML 5 template is used."
    )
  )
  g_out.add_argument(
    '-C', '--css', metavar='FILE', nargs='+', dest='css_files',
    help="include the content of each FILE in it's own `style` tag"
  )
  g_out.add_argument(
    '-J', '--javascript', metavar='FILE', nargs='+', dest='js_files',
    help="include the content of each FILE in it's own `script` tag"
  )
  g_out.add_argument(
    '-M', '--merger', metavar='STRING',
    help="join output of all templates with this STRING"
  )
  g_out.add_argument(
    '--minimize', action='store_true',
    help="minimize output (for HTML)"
  )
  ap.set_defaults(
    template_files=[None],
    verbose=0,
    list=False,
    data_files=[],
    extra={},
    content_files=[],
    css_files=[],
    js_files=[],
    merger='\n',
    minimize=False,
  )
  return ap


def render_templates(context, templates=[None], minimize=False, merger='\n'):
  """
  Returns the output of all rendered *templates* merged with *merger*.

  If *template* is not set, the default :data:`HTML` template is used.

  If *minimize* is set, the rendered results are passed to a **HTML
  minimizer**.

  """
  if not templates or templates == [None]:
    return render(HTML, context, from_string=True, minimize=minimize)
  else:
    output = []
    for template in templates:
      result = render(context, template, minimize=minimize)
      output.append(result)
    return merger.join(output)


def render_template(
  templates=[], content_files=[], data_files=[], css_files=[], js_files=[],
  extra={}, minimize=False, merger='\n'
):
  """
  Returns rendered results build from context.

  """
  context = get_context(
    content_files, data_files, css_files, js_files, minimize, **extra
  )
  return render_templates(context, templates, minimize, merger)


def main(argv=None):
  """
  Parse args, build context and print rendered results.

  """
  # parse arguments
  args = _get_argument_parser().parse_args(argv)
  # verbose output (arguments)
  if args.verbose >= 1:
    print("Arguments\n---------")
    print(args, end='\n\n', file=sys.stderr)
  # list output (and exit)
  if args.list:
    for name, description in KEYWORDS.items():
      print("{}: {}".format(name, description))
    return 0
  # get context
  context = get_context(
    args.content_files, args.data_files, args.css_files, args.js_files,
    args.minimize, **args.extra
  )
  # verbose output (context)
  if args.verbose >= 2:
    print("Context\n---------")
    print(context, end='\n\n', file=sys.stderr)
    # exit now?
    if args.verbose >= 3:
      return 0
  # get output
  output = render_templates(
    context, args.templates, args.minimize, args.merger
  )
  # print output
  print(output.strip())


if __name__ == '__main__':
  sys.exit(main())
