# encoding: UTF-8
# Copyright (C) 2009-2010, Stefan Schwarzer

"""
Converters for several kinds of text files.

See `converter.py` for more on converters.
"""

from __future__ import with_statement

import cgi
import re

import coding
import config
import feature
import tools


def simple_html(doc):
    """Return the document `doc` with an `html` attribute for the HTML
    representation of the document added.
    """
    path = tools.normalize_path(doc.path)
    with open(path) as fobj:
        text = coding.decode(fobj.read())
    escaped_text = cgi.escape(text, quote=True)
    if config.line_numbers:
        numbered_lines = [
          "%4d  %s" % (index+1, line)
          for index, line in enumerate(escaped_text.splitlines())
          if line.strip()]
        escaped_text = "\n".join(numbered_lines)
    doc.html = u"<pre>\n%s\n</pre>" % escaped_text
    doc.mime_type = u"text/html"
    return doc

def highlighted_html(doc):
    """Return the document `doc` with an `html` attribute for the HTML
    representation of the document added. This HTML code has syntax
    highlighting if Pygments can highlight the file type.
    """
    assert feature.pygments, "call this only if Pygments is present"
    import pygments
    from pygments import lexers
    from pygments import formatters
    with open(doc.path) as fobj:
        text = coding.decode(fobj.read())
    try:
        lexer = lexers.guess_lexer_for_filename(doc.path, text)
    except lexers.ClassNotFound:
        # files with many extensions are actually XML files, so
        #  test explicitly for them
        if text.lstrip().startswith(u'<?xml '):
            lexer = lexers.XmlLexer()
        else:
            lexer = lexers.TextLexer()
    formatter = formatters.HtmlFormatter(linenos=config.line_numbers)
    doc.html = pygments.highlight(text, lexer, formatter)
    doc.mime_type = u"text/html"
    return doc

def link_includes_html(doc):
    """Return the document `doc` with an `html` attribute for the HTML
    representation of the document added. This HTML code has include
    or import statements turned into links where possible.
    """
    with open(doc.path) as fobj:
        text = fobj.read()
    def escaped_group(match, group_name):
        return cgi.escape(match.group(group_name))
    new_lines = []
    for line in text.splitlines():
        # try to extract include statements
        match = re.search(
          ur'(?<include>^.*#\s*?include' # `include` statement
           ur"\s+)"                      # some whitespace
          ur'(?<start_delim>[<"])'       # path is enclosed in <> or ""
          ur'(?<path>(?:[^\1]+)?)'       # the path, without the delimiters
          ur'(?<end_delim>[\1>])'        # " if it was found, else the
                                         #  matching > for the <
          ur'(?<rest>.*$)',              # rest of line
          line, re.MULTILINE)
        if match:
            line = u'%s%s<a href="#">%s</a>%s%s' % (
                   escaped_group('include'), escaped_group('start_delim'),
                   escaped_group('path'), escaped_group('end_delim'),
                   escaped_group('rest'))
        else:
            line = cgi.escape(line)
        new_lines.append(line)
        doc.html = u'<pre>\n%s\n</pre>' % \
                   u"\n".join(new_lines)
        doc,mime_type = u"text/html"
        return doc


def hexdump(doc):
    """Return the document `doc` with an `html` attribute containing
    preformatted HTML code for an hexdump of the data under the
    `doc`'s path.
    """
    path = tools.normalize_path(doc.path)
    with open(path, "rb") as fobj:
        data = fobj.read()
    # based on
    #  http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/142812
    filter_ = ''.join(
      [(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])
    length = 16
    result = []
    for i in xrange(0, len(data), length):
        s = data[i:i+length]
        hexa = ' '.join(["%02X" % ord(x) for x in s])
        if len(s) > length // 2:
            hexa = "%s %s" % (hexa[:23], hexa[23:])
        printable = s.translate(filter_)
        result.append("%08X    %-*s    |%s|\n" % (i, length*3, hexa,
                                                  printable))
    escaped_text = cgi.escape("".join(result))
    doc.html = u"<pre>\n%s\n</pre>" % escaped_text
    doc.mime_type = u"text/html"
    return doc

