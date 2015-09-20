# -*- coding: UTF-8 -*-

"""
Basic HTML template.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from . import (
  TemplatorTemplate,
  get_template_from_string,
)


__all__ = ['Template']


template = """<!doctype html>
<html lang="{{ lang|default('en') }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{{ description }}">
  <meta name="keywords" lang="{{ lang|default('en') }}" content="{{ keywords|join(', ') }}">
  {% if keywords_en %}<meta name="keywords" lang="en" content="{{ keywords_en|join(', ') }}">{% endif %}
  <title>{{ title }}</title>
  {% for link in css_links -%}
  <link rel="stylesheet" href="{{ link }}" />
  {%- endfor %}
  {% for css_content in css -%}
  <style>
    {{ css_content }}
  </style>
  {%- endfor %}
  {% for link in js_links -%}
  <script src="{{ link }}"></script>
  {%- endfor %}
  {% for js_content in js -%}
  <script>
    {{ js_content }}
  </script>
  {%- endfor %}
</head>
<body>{{ content }}</body>
</html>"""


Template = TemplatorTemplate(
  name='HTML',
  description='Basic HTML wrapper.',
  template=get_template_from_string(template),
  variables={
    'content': 'contents for the BODY tag',
    'css': 'each element of the list will be put between STYLE tags',
    'css_links': 'each element of the list will be linked from a STYLE tag',
    'description': 'for the site (about two sentences)',
    'js': 'each element of the list will be put between SCRIPT tags',
    'js_links': 'each element of the list will be linked from a SOURCE tag',
    'keywords': 'list of keywords in language `lang`',
    'keywords_en': 'list of keywords in language `en`',
    'lang': 'language code for the site',
    'title': 'string to use as TITLE for the HTML',
  }
)
