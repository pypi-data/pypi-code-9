# -*- coding: UTF-8 -*-

"""
Function to run the module directly or call it programmatically with
:func:`render`.

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import sys
from pprint import pformat

from corelib.templates import (
  render as render_template,
  get_context,
)

from .cli import get_argument_parser
from .templates import (
  get_supported_templates,
  get_template,
  load_templates
)


def render(
  template_files=[], template_string='', template_name=None,
  content_files=[], data_files=[], css_files=[], js_files=[],
  extra={}, minimize=False, merger='\n'
):
  """
  Returns the rendered contents.

  If more than one template is given, the oputput is merged with *merger*.
  If you use HTML templates, their output can be minimized if *minimize* is
  set — Javascript (*js_files*) and CSS (*css_files*) will also be minimized.

  Templates
  ---------

  For the *templates* you can **either**:

  - supply a list of template *template_files* (one or more files)
  - or use a single *template_string*
  - or use one of the default templates with *template_name*.

  Context
  -------

  For the *context* you can:

  - Supply a *content_file* whose contents are directly available in the
    context under ``content`` (MD and RST files are parsed beforehand).

  - Supply a *data_file* whose contents are directly available in the
    context under ``data`` (YAML and JSON files are parsed beforehand).

  - Supply one or more *css_files*, their contents are available in the
    context under ``css``.

  - Supply one or more *js_files*, their contents are available in the
    context under ``js``.

  - At last the extra dictionary is used to update the context.

  .. note::

    If *data_files* or *content_files* have more than than one element, a
    dictionary is created under the key ``data`` / ``content`` where the
    filenames (without ending) point to file`s contents.

  """
  # load templates
  templates = load_templates(template_files, template_string, template_name)
  # build contect
  context = get_context(
    content_files, data_files, css_files, js_files,
    minimize_files=minimize, **extra
  )
  # render templates
  output = [
    render_template(template, context, minimize=minimize)
      for template in templates
  ]
  # merge results
  output = merger.join(output)
  return output


def main(argv=None):
  """
  Parse args and print the results of a :func:`render` call.

  """
  # parse arguments
  args = get_argument_parser().parse_args(argv)
  if args.verbose > 0:
    print("Arguments\n---------")
    agr_string = pformat(args.__dict__)
    print(agr_string, end='\n\n', file=sys.stderr)
    if args.verbose > 1:
      return 0
  # modes?
  if args.list_templates:
    # --- LIST TEMPLATES ---
    templates = get_supported_templates()
    for key in sorted(templates):
      msg = "- {0}: {1.name} — {1.description}".format(key, templates[key])
      print(msg)
  elif args.list_variables:
    # --- LIST TEMPLATE VARIABLES ---
    template = get_template(args.list_variables)
    for key in sorted(template.variables):
      print("- {}: {}".format(key, template.variables[key]))
  elif args.show_context:
    # --- SHOW CONTEXT ---
    context = get_context(
      content_files=args.content_files,
      data_files=args.data_files,
      css_files=args.css_files,
      js_files=args.js_files,
      minimize_files=args.minimize,
      **args.extra
    )
    print(context)
  else:
    # --- RENDER TEMPLATES ---
    output = render(
      template_files=args.template_files,
      template_string=args.template_string,
      template_name=args.template_name,
      content_files=args.content_files,
      data_files=args.data_files,
      css_files=args.css_files,
      js_files=args.js_files,
      extra=args.extra,
      minimize=args.minimize,
      merger=args.merger
    )
    print(output.strip())
  return 0


if __name__ == '__main__':
  sys.exit(main())
