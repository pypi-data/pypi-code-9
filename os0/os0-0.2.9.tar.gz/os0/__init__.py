from . import os0core

os0 = os0core.Os0(doinit=True)


def nakedname(fn):
    """Return nakedename (without extension)"""
    i = fn.rfind('.')
    if i >= 0:
        j = len(fn) - i
        if j <= 4:
            fn = fn[:i]
    return fn
