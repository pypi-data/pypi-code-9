# -*- coding: utf-8 -*-
VERSION = (0, 0, 1, 'beta', 1)

def get_version(*args, **kwargs):
    # Don't litter django/__init__.py with all the get_version stuff.
    # Only import if it's actually called.
    from ipapi.version import get_version
    return get_version(*args, **kwargs)

__version__ = get_version()
