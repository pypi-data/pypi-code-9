from django.db.models import AutoField
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import PositiveSmallIntegerField

from localization.models import LocalizableObjectBase
from localization.models import LocalizableValueBase


class Holiday(LocalizableObjectBase):
    id                  = AutoField(                               blank=False, unique=False, primary_key=True)
    country             = ForeignKey('locations.Country',          blank=False, unique=False, null=True, related_name='+')
    code                = CharField(                               blank=False, unique=True,  max_length=64)
    recurrent_month     = PositiveSmallIntegerField(               blank=False, unique=False)
    recurrent_day       = PositiveSmallIntegerField(               blank=False, unique=False)

    def _get_name(self):
        return self._get_localizable_value(self.names, 'name', '')

    def _set_name(self, value):
        self._set_localizable_value(self.names, 'name', value)

    def _del_name(self,):
        self._del_localizable_value(self.names, 'name')

    name = property(_get_name, _set_name, _del_name)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name        = 'Holiday'
        verbose_name_plural = 'Holidays'


class HolidayName(LocalizableValueBase):
    localizable_object  = ForeignKey(Holiday,                      blank=False, unique=False, related_name='names')


class HolidayException(Model):
    id                  = AutoField(                               blank=False, unique=False, primary_key=True)
    holiday             = ForeignKey(Holiday,                      blank=False, unique=False, null=True, related_name='+')
    date                = DateField(                               blank=False, unique=False)

    def __str__(self):
        return "%s @ %s" % (self.holiday, self.date)

    class Meta:
        unique_together     = [('holiday', 'date', 'id', )]
        verbose_name        = 'Holiday Exception'
        verbose_name_plural = 'Holiday Exceptions'
