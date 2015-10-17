# encoding: UTF-8
# Copyright (C) 2007-2010, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
Various utilities which don't fit into other modules.

Some of the code here helps to sanitize file system paths in an
attempt to prevent unintended information disclosure.
"""

import os
import re

import config


class NotUnderRoot(Exception):
    pass


def normalize_path(path):
    """Return the file system path `path` in "normalized" form:

    - change each sequence of path separators to a single path separator
    - change path by evaluating "." and ".." occurences
    - make path absolute
    """
    # maybe remove this later
    assert isinstance(path, unicode), "not a unicode string: %r" % path
    # strange workaround for backslash separator; else doesn't seem to work
    if os.sep == "\\":
        replacement = "\\\\"
    else:
        replacement = os.sep
    path = re.sub(u"(?:%s)+" % re.escape(os.sep), replacement, path)
    # in some special cases `normpath` returns byte strings even if
    #  the argument was a unicode string, so convert "manually"
    path = unicode(os.path.normpath(path))
    path = os.path.normcase(path)
    # in some special cases `abspath` returns byte strings even if
    #  the argument was a unicode string, so convert "manually"
    return unicode(os.path.abspath(path))

def is_file_system_root(path):
    r"""Return `True` if the unicode string `path` is a file system
    root directory, else `False`.

    Under Posix, the file system root directory is "/", under
    Windows, it's r"x:\", where x is any drive letter.
    """
    path = normalize_path(path)
    drive, rest = os.path.splitdrive(path)
    return rest == os.sep

def is_safe_path(path, root):
    """Return `True` if the `path` is a subdirectory of or a file
    under the document root directory `root`, else return `False`.
    Also return `False` if the path matches any of the patterns to
    ignore.

    Both `path` and `root` must be unicode strings.
    """
    path = normalize_path(path)
    if config.ignore_path(path):
        return False
    root = normalize_path(root)
    if path == root:
        return True
    if is_file_system_root(root):
        return path.startswith(root)
    else:
        return path.startswith(root + os.sep)

def path_to_title(path, root):
    """Return an unicode title string from `path` and `root`.

    Here, `root` determines the root directory below which `path`
    is located. The title is meant to be used as the title of a
    directory or file frame.

    Note the role of the argument `root` in the following examples:

    >>> path_to_title(u"/my/root/some/where/below", u"/my/root")
    u'some/where/below'
    >>> path_to_title(u"/my/root/some/where/below", u"/my/root/some")
    u'where/below'

    If the `path` isn't part of the `root`, raise a `NotUnderRoot`
    exception.
    """
    path = normalize_path(path)
    root = normalize_path(root)
    if not is_safe_path(path, root):
        raise NotUnderRoot('path "%s" isn\'t under root directory "%s"' %
                           (path, root))
    title = path.replace(root, "", 1)
    if title:
        return title[1:]
    else:
        return u"."

def sequence_to_url(sequence, absolute=False):
    """Return a sequence converted to an absolute or relative URL.
    If `absolute` is true, the result is an absolute URL, else it's
    a relative URL. The result is of type unicode if any of the
    items in `sequence` is a unicode string. Otherwise, the result
    is a bytestring.
    """
    relative_path = "/".join(sequence)
    if absolute:
        return "/" + relative_path
    else:
        return relative_path

