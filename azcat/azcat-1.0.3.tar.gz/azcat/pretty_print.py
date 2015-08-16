import os
import json

import pygments
import pygments.lexers
import pygments.formatters

from azcat.guess_ext import guess_ext_by_contents, guess_ext_by_filename

def load_module (type_, name):
    try:
        m = getattr(getattr(__import__("azcat.{0}.{1}".format(type_, name)), type_), name)
    except ImportError:
        return None
    return m

def _load_formatter (name):
    return load_module("formatters", name)

def _load_highlighter (name):
    return load_module("highlighters", name)


def pretty_print (src, s, out, with_formatter, ext=None):
    """ `src' is a filepath to be formatted. `out' is a file object
        to be written."""

    if ext == "h":
        ext = "c" # XXX: Pygments does not highlight .h files
    elif ext is None:
        ext = guess_ext_by_filename(src)
        if ext == "":
            ext = guess_ext_by_contents(s)

    # format
    if with_formatter:
        f = _load_formatter(ext)
        if f is not None:
            ext,s = f.format(s)

    # highlight
    h = _load_highlighter(ext)
    if h is None:
        try:
            lexer = pygments.lexers.get_lexer_by_name(ext)
        except pygments.util.ClassNotFound:
            lexer = pygments.lexers.get_lexer_for_mimetype("text/plain")
        fmt = pygments.formatters.Terminal256Formatter(encoding="utf-8")
        pygments.highlight(s, lexer, fmt, out)
    else:
        h.highlight(out, s)
        out.close()
