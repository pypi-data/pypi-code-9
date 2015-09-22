#-*- coding: utf-8 -*-

from sqlalchemy import Column as _Column, String as _String, Boolean as _Boolean, Text as _Text, DATETIME as _DateTime, TIMESTAMP as _TimeStamp
from sqlalchemy.dialects.mysql import INTEGER as _Integer

__all__ = ['Column', 'String', 'Integer', 'Boolean', 'Text', 'DateTime', 'TimeStamp']


class Column(_Column):
    pass


class String(_String):
    pass


class Integer(_Integer):
    pass


class Boolean(_Boolean):
    pass


class Text(_Text):
    pass


class DateTime(_DateTime):
    pass


class TimeStamp(_TimeStamp):
    pass
