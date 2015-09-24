# -*- coding: utf-8 -*-
from sqlalchemy import Column as SaColumn
from sqlalchemy.sql.elements import Label as SaLabel
from sqlalchemy.ext.declarative.api import DeclarativeMeta
__author__ = 'vahid'


def extract_columns(obj):
    if isinstance(obj, DeclarativeMeta):
        for c in obj.__table__.c.values():
            yield c.name, c
    else:
        for descr in obj.column_descriptions:
            expr = descr['expr']
            if isinstance(expr, SaLabel):
                yield expr.key, expr.element
            elif issubclass(descr['type'].__class__, DeclarativeMeta):
                for c in expr.__table__.c:
                    if isinstance(c, SaColumn):
                        yield c.name, c
            elif expr.is_attribute:
                yield expr.key, getattr(expr.class_, expr.key)
