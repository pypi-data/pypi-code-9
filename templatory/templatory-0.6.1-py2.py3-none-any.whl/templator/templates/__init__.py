# -*- coding: UTF-8 -*-

"""
Collects default templates.

All available templates must be added as :cls:`TemplatorTemplate` named tuple
to the data:`SUPPORTED_TEMPLATES` dictionary under an available key.


TemplatorTemplate
-----------------

:name: the name of the template
:description: a description of the template
:template: the JINJA template
:variables: dictionary with `variable -> explanation` pairs for the context

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from collections import namedtuple

from corelib.templates import load_template


__all__ = [
  'TemplatorTemplate',
  'SUPPORTED_TEMPLATES',
  'get_template_from_string',
  'get_supported_templates',
  'get_template',
  'load_templates',
]


TemplatorTemplate = namedtuple(
  'Template', [
    'name',
    'description',
    'template',
    'variables',
  ]
)


def get_template_from_string(template_string):
  """
  Returns a JINJA template from *template_string*.

  """
  return load_template(template_string, from_string=True)


from .html import Template as html


SUPPORTED_TEMPLATES = {
  'html': html,
}


def get_supported_templates():
  """
  Returns a copy of the :data:`SUPPORTED_TEMPLATES` dictionary.

  """
  return SUPPORTED_TEMPLATES.copy()


def get_template(name='html'):
  """
  Returns the :cls:`TemplatorTemplate` with *name*.

  :raises KeyError: if *name* is not supported.

  """
  try:
    return SUPPORTED_TEMPLATES[name]
  except KeyError:
    msg = "unknown template '{}'. Available templates are : {}."
    msg = msg.format(name, ', '.join(sorted(SUPPORTED_TEMPLATES.keys())))
    raise KeyError(msg)


def load_templates(template_files=[], template_string='', template_name=None):
  """
  Returns a list of JINJA templates.

  You can **either**:

  - supply a list of template *template_files* (one or more files)
  - or use a single *template_string*
  - or use one of the default templates with *template_name*.

  Only those templates availabel by the :func:`get_template` function (see
  :data:`SUPPORTED_TEMPLATES`) are supported for *template_name*.

  If none is given, a list containing only the default template is returned.

  :raises ValueError: on wrong arguments.

  """
  if len(
    list(filter(None, (template_files, template_string, template_name)))
  ) > 1:
    msg = (
      "You can either supply template files, use one of the default "
      "templates, or supply templates as string — but you can't mix those."
    )
    raise ValueError(msg)
  if template_files:
    templates = [load_template(filename) for filename in template_files]
  else:
    if template_string:
      template = get_template_from_string(template_string)
    else:
      if template_name:
        template = get_template(template_name).template
      else:
        template = get_template().template
    templates = [template]
  return templates
