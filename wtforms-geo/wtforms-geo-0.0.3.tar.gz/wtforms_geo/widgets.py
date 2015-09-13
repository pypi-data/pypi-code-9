# -*- coding: utf-8 -*-
"""
    wtfgeo.widgets
    ==============

    :copyright: (c) 2015 by Erle Carrara.
    :license: BSD, see LICENSE for more details.
"""

import json
from wtforms.widgets import Input, HTMLString


class GeometryEditor(Input):

    input_type = 'hidden'

    attribution = 'Map data &copy; <a href="http://openstreetmap.org">' \
                  'OpenStreetMap</a> contributors'

    shapes = ['polyline', 'rectangle', 'circle', 'marker']

    def _update_options(self, options):
        if options:
            for key, value in options.items():
                if key in self.options and isinstance(self.options[key], dict):
                    self.options[key].update(value)
                else:
                    self.options[key] = value

    def __init__(self, **kwargs):
        self.options = {
            'toolbar': {
                'draw': {
                    'polyline': False,
                    'polygon': False,
                    'rectangle': False,
                    'circle': False,
                    'marker': False
                },
                'edit': {
                    'remove': {},
                    'edit': {}
                }
            },
            'center': None,
            'zoom': None,
            'max': None,
            'baselayer': {
                'url': 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                'options': {
                    'attribution': self.attribution
                }
            }
        }

        self._update_options(kwargs)

    def __call__(self, field, options=None, **kwargs):
        for shape in self.shapes:
            self.options['toolbar']['draw'][shape] = {}

        self._update_options(options)

        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('data-geometry-editor', True)
        kwargs.setdefault('data-options', json.dumps(self.options))

        if 'value' not in kwargs:
            kwargs['value'] = HTMLString(field._value())

        params = self.html_params(name=field.name, **kwargs)
        return HTMLString('<input {0}>'.format(params))


class PolylineEditor(GeometryEditor):
    shapes = ['polyline']


class PolygonEditor(GeometryEditor):
    shapes = ['polygon']


class RectangleEditor(GeometryEditor):
    shapes = ['rectangle']


class CircleEditor(GeometryEditor):
    shapes = ['circle']


class PointEditor(GeometryEditor):
    shapes = ['marker']
