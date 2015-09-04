# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import re
import pytz
from django.conf import settings
from hipster_api.fields.str import String as _String
from hipster_api.fields.number import Integer as _Integer


class DateTime(_String):
    def __init__(self, date_format=None, now=False, timezone=None, **kwargs):
        self.date_format = date_format or '%Y-%m-%d %H:%M:%S'
        self.now = now
        self.timezone_default = timezone or getattr(settings, 'TIME_ZONE', 'Europe/Moscow')
        self.timezone = self.timezone_default
        super(DateTime, self).__init__(**kwargs)

    def __timezone(self):
        timezone = re.search(r'(\(\w+/\w+\))', self.value, re.IGNORECASE)
        if timezone:
            self.timezone = timezone.group(0)[1:-1]
            self.setitem(self.value.replace('(%s)' % self.timezone, ''))
        else:
            self.timezone = self.timezone_default

        return pytz.timezone(self.timezone)

    def to_python(self):
        super(DateTime, self).to_python()
        timezone = self.__timezone()
        value = self.value

        if self.now:
            return self.setitem(datetime.datetime.now())
        try:
            value = datetime.datetime.strptime(value, self.date_format).replace(tzinfo=timezone)
        except ValueError:
            if hasattr(self.default, '__call__'):
                return self.setitem(self.default())
            try:
                value = datetime.datetime.strptime(self.default, self.date_format).replace(tzinfo=timezone)
            except ValueError:
                value = datetime.datetime.now(timezone)
        self.setitem(value)


class Date(DateTime):
    def __init__(self, **kwargs):
        kwargs['date_format'] = '%Y-%m-%d' if 'date_format' not in kwargs else kwargs['date_format']
        super(Date, self).__init__(**kwargs)

    def to_python(self):
        super(Date, self).to_python()
        try:
            self.setitem(self.value.date())
        except AttributeError:
            self.setitem(self.value)


class Boolean(_Integer):
    def to_python(self):
        self.setitem(bool(super(Boolean, self).to_python()))
