# coding=utf8

"""
    kks.parser
    ~~~~~~~~~~

    Parser from post source to html.
"""

from datetime import datetime
import os

from . import charset, src_ext
from .exceptions import *
import libparser

import houdini
import misaka as m
from misaka import HtmlRenderer, SmartyPants

src_ext_len = len(src_ext)  # cache this, call only once

to_unicode = lambda string: string.decode(charset)


# Create a custom renderer
class BleepRenderer(HtmlRenderer, SmartyPants):
    def block_code(self, text, lang):
        text = text.encode(charset).strip()
        return '\n<pre><code>%s</code></pre>\n' % \
            houdini.escape_html(text.strip())

class Parser(object):
    """Usage::

        parser = Parser()
        parser.parse(str)   # return dict
        parser.markdown.render(markdown_str)  # render markdown to html

    """

    def __init__(self):
        """Initialize the parser, set markdown render handler as
        an attribute `markdown` of the parser"""

        renderer = BleepRenderer()
        self.markdown = m.Markdown(renderer,
            extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)

    def parse_markdown(self, markdown):
        return self.markdown.render(markdown)

    def parse(self, source):
        """Parse ascii post source, return dict"""

        rt, title, title_pic, markdown = libparser.parse(source)

        if rt == -1:
            raise SeparatorNotFound
        elif rt == -2:
            raise PostTitleNotFound

        # change to unicode
        title, title_pic, markdown = map(to_unicode, (title, title_pic,
                                                      markdown))

        # render to html
        html = self.markdown.render(markdown)
        summary = self.markdown.render(markdown[:200])

        return {
            'title': title,
            'markdown': markdown,
            'html': html,
            'summary': summary,
            'title_pic': title_pic
        }

    def parse_filename(self, filepath):
        """parse post source files name to datetime object"""
        name = os.path.basename(filepath)[:-src_ext_len]
        try:
            dt = datetime.strptime(name, "%Y-%m-%d-%H-%M")
        except ValueError:
            raise PostNameInvalid
        return {'name': name, 'datetime': dt, 'filepath': filepath}


parser = Parser()  # build a runtime parser
