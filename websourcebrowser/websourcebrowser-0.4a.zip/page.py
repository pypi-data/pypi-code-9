# encoding: UTF-8
# Copyright (C) 2008-2009, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
This module takes care of rendering the HTML for the left and right
pane and the complete page.
"""

from __future__ import with_statement

import cgi
import os

import config
import converter
import directory_converter
import document
import template
import tools


def top_pane_html(path):
    """Return HTML code as a unicode string for the top pane."""
    version = config.VERSION
    path = tools.path_to_title(path, config.root)
    path = cgi.escape(path)
    return template.TOP % locals()

def directory_pane_html(path):
    """Return HTML code as a unicode string for the left pane."""
    dir_doc = document.Document(path=path)
    try:
        content = directory_converter.treeview_html(dir_doc).html
    except IOError, exc:
        raise converter.InvalidPath('invalid path "%s"' % path)
    return template.DIRECTORY % locals()

def file_pane_html(path):
    """Return HTML code as a unicode string for the right pane."""
    path = tools.normalize_path(path)
    doc = document.Document(path=path)
    converter_ = converter.converter(path)
    content = converter_(doc).html
    assert doc.mime_type is not None, u"MIME type of document not set"
    return template.FILE % locals()

def page_html(path):
    """Return HTML code for the whole page as a unicode string."""
    path = tools.normalize_path(path)
    top = top_pane_html(path)
    dir_ = directory_pane_html(config.root)
    file_ = file_pane_html(path)
    title = tools.path_to_title(path, config.root)
    project_title = config.project_title
    static_dir = config.STATIC_DIR
    return template.PAGE % locals()


if __name__ == "__main__":
    import os
    p = Page(unicode(os.path.curdir), u"page.py")
    print p.as_html()

