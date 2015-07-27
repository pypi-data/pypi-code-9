#!/usr/bin/env python3
"""
Module _SEQ -- Enhanced sequence classes
Sub-Package STDLIB.COLL of Package PLIB3
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the ``namedsequence`` and ``typed_namedsequence``
classes, which are similar to their ``namedtuple`` counterparts
but have writable fields.
"""

import sys
from plib.stdlib.coll import abstractsequence

from ._names import process_names, process_specs

__all__ = [
    'namedsequence',
    'typed_namedsequence'
]


class _seq(abstractsequence):
    
    _fields = None
    
    def __init__(self, iterable=None):
        # Storage for actual values; fill in with defaults so the
        # __setitem__ code will work when we populate from iterable
        # below (uses __getitem__ to validate indexes)
        self._items = {f: "" for f in self._fields}
        
        # Now we can populate from the given iterable
        if iterable:
            for index, item in enumerate(iterable):
                self[index] = item
    
    def __len__(self):
        return len(self._fields)
    
    def __getitem__(self, index):
        return getattr(self, self._fields[index])
    
    def set_index(self, index, value):
        setattr(self, self._fields[index], value)


def _make_prop(i, name, conv=None):
    def _get(self):
        return self._items[name]
    if conv:
        def _set(self, value):
            self._items[name] = conv(value)
    else:
        def _set(self, value):
            self._items[name] = value
    _doc = "Alias for field number {:d}".format(i)
    return property(_get, _set, doc=_doc)


def _make_seq(typename, attrs, _doc):
    
    attrs.update({
        '__doc__': _doc
    })
    
    result = type(_seq)(typename, (_seq,), attrs)
    try:
        result.__module__ = sys._getframe(2).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass
    return result


def namedsequence(typename, field_names, rename=False):
    field_names, _doc = process_names(typename, field_names, rename)
    attrs = {
        '_fields': field_names
    }
    
    for i, field_name in enumerate(field_names):
        attrs.update({
            field_name: _make_prop(i, field_name)
        })
    
    return _make_seq(typename, attrs, _doc)


def typed_namedsequence(typename, fieldspecs, rename=False):
    fieldspecs, field_names, field_types, field_specs, _doc = process_specs(typename, fieldspecs, rename)
    attrs = {
        '_fields': field_names,
        '_fieldtypes': field_types,
        '_fieldspecs': field_specs
    }
    
    for i, (field_name, field_type) in enumerate(field_specs):
        attrs.update({
            field_name: _make_prop(i, field_name, field_type)
        })
    
    return _make_seq(typename, attrs, _doc)
