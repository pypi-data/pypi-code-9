from plone.formwidget.geolocation.geolocation import Geolocation
from plone.formwidget.geolocation.interfaces import IGeolocation
from plone.formwidget.geolocation.interfaces import IGeolocationField
from zope import schema
from zope.interface import implements


class GeolocationField(schema.Object):
    implements(IGeolocationField)

    _type = Geolocation
    schema = IGeolocation

    def __init__(self, **kw):
        super(GeolocationField, self).__init__(schema=self.schema, **kw)
