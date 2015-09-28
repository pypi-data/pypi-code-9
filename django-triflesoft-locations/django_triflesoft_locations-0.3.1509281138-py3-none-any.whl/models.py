from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import Manager
from django.db.models import PositiveIntegerField

from localization.models import LocalizableObjectBase
from localization.models import LocalizableValueBase


class CountryManager(Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Country(LocalizableObjectBase):
    objects = CountryManager()

    id                  = PositiveIntegerField(                    blank=False, unique=True,  primary_key=True, help_text="<a href='http://en.wikipedia.org/wiki/ISO_3166-1_numeric'>ISO 3166-1</a>")
    code                = CharField(                               blank=False, unique=True,  max_length=2,     help_text="<a href='http://en.wikipedia.org/wiki/ISO_3166-2'>ISO 3166-2</a>")
    is_published        = BooleanField(                            blank=False, unique=False, default=False)

    def natural_key(self):
        return (self.code, )

    def _get_name(self):
        return self._get_localizable_value(self.names, 'name', '')

    def _set_name(self, value):
        self._set_localizable_value(self.names, 'name', value)

    def _del_name(self,):
        self._del_localizable_value(self.names, 'name')

    name = property(_get_name, _set_name, _del_name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Country'
        verbose_name_plural = 'Countries'


class CountryName(LocalizableValueBase):
    localizable_object  = ForeignKey(Country,                      blank=False, unique=False, related_name='names')


class RegionManager(Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Region(LocalizableObjectBase):
    objects = RegionManager()

    id                  = PositiveIntegerField(                    blank=False, unique=False, primary_key=True, help_text='Phone Code')
    country             = ForeignKey(Country,                      blank=False, unique=False, related_name='+')
    code                = CharField(                               blank=False, unique=False, max_length=64,    help_text='Phone Code')
    time_zone           = IntegerField(                            blank=False, unique=False)
    is_published        = BooleanField(                            blank=False, unique=False, default=False)

    def natural_key(self):
        return (self.code, )

    def _get_name(self):
        return self._get_localizable_value(self.names, 'name', '')

    def _set_name(self, value):
        self._set_localizable_value(self.names, 'name', value)

    def _del_name(self,):
        self._del_localizable_value(self.names, 'name')

    name = property(_get_name, _set_name, _del_name)

    def __str__(self):
        return self.name

    class Meta:
        unique_together     = [('country', 'code')]
        verbose_name        = 'Region'
        verbose_name_plural = 'Regions'


class RegionName(LocalizableValueBase):
    localizable_object  = ForeignKey(Region,                       blank=False, unique=False, related_name='names')
