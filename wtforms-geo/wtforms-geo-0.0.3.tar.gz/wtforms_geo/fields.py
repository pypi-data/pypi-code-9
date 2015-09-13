# -*- coding: utf-8 -*-
"""
    wtfgeo.fields
    =============

    :copyright: (c) 2015 by Erle Carrara.
    :license: BSD, see LICENSE for more details.
"""

import geojson
from shapely.geometry import shape
from geoalchemy2.shape import to_shape, from_shape
from wtforms.fields import Field
from wtforms_geo.widgets import (GeometryEditor,
                                 PolylineEditor,
                                 PolygonEditor,
                                 RectangleEditor,
                                 CircleEditor,
                                 PointEditor)


class GeometryField(Field):

    WGS84_SRID = 4326

    widget = GeometryEditor()

    def __init__(self, label='', validators=None, srid=WGS84_SRID,
                 only_one=True, widget_options=None, **kwargs):
        super(GeometryField, self).__init__(label, validators, **kwargs)
        self.data = None
        self.srid = srid
        self.only_one = only_one
        self.widget_options = widget_options or {}

    def __call__(self, **kwargs):
        if self.only_one:
            self.widget_options['max'] = 1

        return self.widget(self, options=self.widget_options, **kwargs)

    def _value(self):
        if self.data is not None:
            if not isinstance(self.data, list):
                self.data = [self.data]

            return geojson.dumps({
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'properties': {},
                    'geometry': to_shape(wkb_element)
                } for wkb_element in self.data]
            })

        return u''

    def process_data(self, value):
        self.data = value

    def process_formdata(self, valuelist):
        if not valuelist:
            self.data = None
            return

        self.data = []
        geo = geojson.loads(valuelist[0])
        for feature in geo.features:
            if feature.geometry:
                self.data.append(from_shape(shape(feature.geometry)))

        if self.only_one:
            self.data = self.data[0] if len(self.data) > 0 else None


class PolylineField(GeometryField):
    widget = PolylineEditor()


class PolygonField(GeometryField):
    widget = PolygonEditor()


class RectangleField(GeometryField):
    widget = RectangleEditor()


class CircleField(GeometryField):
    widget = CircleEditor()


class PointField(GeometryField):
    widget = PointEditor()
