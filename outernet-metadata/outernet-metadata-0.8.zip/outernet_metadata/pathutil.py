"""
Functions for working with paths

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import os


def fnwalk(path, fn):
    """
    Walk directory tree top-down until directories of desired length are found

    This generator function takes a ``path`` from which to begin the traversal,
    and a ``fn`` object that selects the paths to be returned. It calls
    ``os.listdir()`` recursively until either a full path is flagged by ``fn``
    function as valid (by returning a truthy value) or ``os.listdir()`` fails
    with ``OSError``.

    This function has been added specifically to deal with large and deep
    directory trees, and it's tehrefore not avisable to convert the return
    values to a lists and similar memory-intensive objects.
    """
    if fn(path):
        yield path

    try:
        names = os.listdir(path)
    except OSError:
        return

    for name in names:
        for child in fnwalk(os.path.join(path, name), fn):
            yield child


def extwalk(path, exts=['.jpg', '.jpeg', '.png', '.gif', '.svg']):
    """
    Walk directory tree top-down until files with given extensions are matched.

    Default set of extensions match common image formats including SVG. The
    extension list can be customized by providing a non-generator iterable
    (e.g., list, tuple, dict) where each memeber is an extension including the
    dot.
    """
    matchfn = lambda p: os.path.isfile(p) and os.path.splitext(p)[1] in exts
    for p in fnwalk(matchfn):
        yield p


def extcount(path, exts=['.jpg', '.jpeg', '.png', '.gif', '.svg']):
    """
    Return a count of all files matching given extensions in a certain path

    Default set of extensions match common image formats including SVG. The
    extension list can be customized by providing a non-generator iterable
    (e.g., list, tuple, dict) where each memeber is an extension including the
    dot.
    """
    if os.path.isfile(path):
        return os.path.splitext(path)[1] in exts
    sub = os.listdir(path)
    total_found = 0
    for s in sub:
        total_found += extcount(os.path.join(path, s), exts)
    return total_found
