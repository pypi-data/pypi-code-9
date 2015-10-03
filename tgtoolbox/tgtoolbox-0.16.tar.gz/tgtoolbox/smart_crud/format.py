# -*- coding: utf-8 -*-
from datetime import datetime
from khayyam import JalaliDatetime
from tg import request
__author__ = 'vahid'

class Formatter(object):
    def __init__(self, value):
        self.value = value

    def format_datetime(self):
        if request and hasattr(request, 'language') and request.language.startswith('fa'):
            dt = JalaliDatetime.from_datetime(self.value)
        else:
            dt = self.value
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def __unicode__(self):
        if not self.value:
            return ''
        if isinstance(self.value, datetime):
            value = self.format_datetime()
        else:
            value = self.value
        return value