# -*- coding: utf-8 -*-
import re
import os
import os.path


class CommaSeparatedList(object):
    def __init__(self, string):
        self.items = [v.strip() for v in string.split(',')]

    def __contains__(self, item):
        return item in self.items


def ensure_dirs(path):
    """ Make sure all ancestors of *path* exist, create them otherwise. """
    dirpath = os.path.dirname(path)

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    elif not os.path.isdir(dirpath):
        raise IOError("ensure_dirs(): parent directory is not a directory")


def cstr(text, nocolors=False):
    """ Helper function for coloring strings for output in shell.

    :arg text:      Color formatted string to convert to shell colors.
    :arg nocolors:  If set to ``True`` all color codes will be removed from
                    *text* but not replaced by the shell codes. Defaults
                    to ``False``.

    The *text* should be formatted using ``^`` symbol followed by the shell
    code. So ``\e[33m`` becomes ``^33``.
    """
    def on_sub(m):
        if nocolors:
            return m.group(1)
        else:
            return m.group(1) + "\033[{}m".format(m.group('code'))

    pttrn = r'([^^]|^)(\^(?P<code>[130]\d?))'
    while re.search(pttrn, text):
        text = re.sub(pttrn, on_sub, text)
    return text.replace("^^", "^")

