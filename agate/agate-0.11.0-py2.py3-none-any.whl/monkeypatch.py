#!/usr/bin/env python

import inspect

def monkeypatch(cls, patch):
    methods = inspect.getmembers(patch, predicate=inspect.ismethod)

    print methods
