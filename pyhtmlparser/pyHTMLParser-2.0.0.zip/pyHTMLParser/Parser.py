# Copyright (c) 2015 Jun Ishibashi
#
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without 
# restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following 
# conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE 
# OR OTHER DEALINGS IN THE SOFTWARE.

from urllib.request import *
from html.parser import HTMLParser
import re

from pyHTMLParser.ParserUtils import is_self_closing
from pyHTMLParser.pyNode import pyNode, pyNodeList

def url_checker(url):
    result = re.match('^http[s]?://', url)
    if result == None: return False
    else: return True
    
class Parser(HTMLParser):

    def __init__(self, url=None):
        super(self.__class__, self).__init__(convert_charrefs = True)
        if url != None:
            if not url_checker(url):
                raise ValueError('Url must start with http:// or https://')
            else:
                self._url = url
        else:
            self._url = None
        self._dom = []
        self._nodes = pyNodeList()
        self._decoder = 'utf-8'

    def __getitem__(self, fn):
        if fn == 'select_attr_contains_prefix':
            return self.select_attr_contains_prefix
        elif fn == 'select_attr_contains':
            return self.select_attr_contains
        elif fn == 'select_attr_contains_word':
            return self.select_attr_contains_word
        elif fn == 'select_attr_ends_with':
            return self.select_attr_ends_with
        elif fn == 'select_attr_not_equal':
            return self.select_attr_not_equal
        elif fn == 'select_attr_starts_with':
            return self.select_attr_starts_with
        elif fn == 'first':
            return self.first
        elif fn == 'last':
            return self.last
        elif fn == 'even':
            return self.even
        elif fn == 'odd':
            return self.odd
        elif fn == 'select_button':
            return self.select_button
        elif fn == 'select_checkbox':
            return self.select_checkbox
        elif fn == 'select_checked':
            return self.select_checked
        elif fn == 'select_disabled':
            return self.select_disabled
        elif fn == 'select_empty':
            return self.select_empty
        elif fn == 'select_enabled':
            return self.select_enabled
        elif fn == 'select_file':
            return self.select_file
        elif fn == 'select_first_child':
            return self.select_first_child
        elif fn == 'select_last_child':
            return self.select_last_child
        elif fn == 'select_first_of_type':
            return self.select_first_of_type
        elif fn == 'select_last_of_type':
            return self.select_last_of_type
        elif fn == 'select_image':
            return self.select_image
        elif fn == 'select_input':
            return self.select_input
        elif fn == 'eq':
            return self.eq
        elif fn == 'gt':
            return self.gt
        elif fn == 'lt':
            return self.lt
        elif fn == 'select_nth_child':
            return self.select_nth_child
        elif fn == 'select_nth_last_child':
            return self.select_nth_last_child
        elif fn == 'select_nth_last_of_type':
            return self.select_nth_last_of_type
        elif fn == 'select_nth_of_type':
            return self.select_nth_of_type
        elif fn == 'not_':
            return self.not_
        elif fn == 'select_has':
            return self.select_has
        elif fn == 'header':
            return self.header
        elif fn == 'select_only_child':
            return self.select_only_child
        elif fn == 'select_only_of_type':
            return self.select_only_of_type
        elif fn == 'select_parent':
            return self.select_parent
        elif fn == 'select_password':
            return self.select_password
        elif fn == 'select_radio':
            return self.select_radio
        elif fn == 'select_reset':
            return self.select_reset
        elif fn == 'select_root':
            return self.select_root
        elif fn == 'select_selected':
            return self.select_selected
        elif fn == 'select_submit':
            return self.select_submit
        elif fn == 'select_text':
            return self.select_text

    def set_decoding(self, dec):
        self._decoder = dec

    def open(self, url=None):
        if url != None:
            if not url_checker(url):
                raise ValueError('Url must start with http:// or https://')
            else:
                self._url = url
        else:
            if self._url == None:
                raise ValueError('Url is empty')
        try:
            res = urlopen(self._url)
        except Exception:
            raise Exception('Error connecting at %s' % self._url)
        self._html = res.read().decode(self._decoder)
        res.close()

    def construct(self):
        self.feed(self._html)

    def close(self):
        super(self.__class__, self).close()

    def clear(self):
        self._html = ''
        self._url = None
        self._nodes = pyNodeList()
        del self._dom[:]

    def set_html(self, html):
        self._html = html;

    def raw_html(self):
        return self._html

    def tag(self, tag):
        ret = pyNodeList()
        for node in self._nodes:
            if node.name() == tag.lower():
                ret.append(node)
        return ret

    def id(self, i):
        return self._nodes.id(i)

    def cls(self, c):
        return self._nodes.cls(c)

    def header(self):
        ret = pyNodeList()
        h = list()
        h.append(self._nodes.tag('h1'))
        h.append(self._nodes.tag('h2'))
        h.append(self._nodes.tag('h3'))
        h.append(self._nodes.tag('h4'))
        h.append(self._nodes.tag('h5'))
        h.append(self._nodes.tag('h6'))
        for elem in h:
            if isinstance(elem, pyNodeList) and len(elem) != 0:
                ret.extend(elem)
            elif isinstance(elem, pyNode):
                ret.append(elem)
        return ret

    def handle_starttag(self, tag, attrs):
        node = pyNode(tag.lower())
        if len(self._dom) != 0:
            node.set_parent(self._dom[-1])
            self._dom[-1].add_child(node)
        if not is_self_closing(tag.lower()):
            self._dom.append(node)
        self._nodes.append(node)
        for attr in attrs:
            node.set_attr(attr[0], attr[1])
                    
    def handle_endtag(self, tag):
        if self._is_started:
            self._dom.pop()
            if tag == 'html':
                self._is_started = False
                assert len(self._dom) == 0, 'dom stack is not empty'
            else:
                assert len(self._dom) != 0, 'dom stack is empty but parsing has not ended'

    def handle_startendtag(self, tag, attrs):
        node = pyNode(tag.lower())
        if len(self._dom) != 0:
            node.set_parent(self._dom[-1])
            self._nodes.append(node)
        for attr in attrs:
            node.set_attr(attr[0], attr[1])

    def handle_data(self, data):
        if self._is_started:
            text = data.replace('\r\n', '')
            text = text.replace('\n', '')
            text = text.replace('\t', '')
            self._dom[-1].add_text(text.strip())

    def handle_comment(self, data):
        if self._is_started:
            node = pyNode('comment')
            node.set_parent(self._dom[-1])
            self._dom[-1].add_child(node)
            node.add_comment(data)

    def first(self):
        return self._nodes.first()

    def last(self):
        return self._nodes.last()

    def eq(self, index):
        return self._nodes.eq(index)

    def even(self):
        return self._nodes.even()

    def odd(self):
        return self._nodes.odd()

    def gt(self, index):
        return self._nodes.gt(index)

    def lt(self, index):
        return self._nodes.lt(index)

    def contains(self, text):
        return self._nodes.contains(text)

    def not_(self, pynodelist):
        return self._nodes.not_(pynodelist)

    def select_button(self):
        return self._nodes.select_button()

    def select_checkbox(self):
        return self._nodes.select_checkbox()

    def select_checked(self):
        return self._nodes.select_checked()

    def select_disabled(self):
        return self._nodes.select_disabled()

    def select_empty(self):
        return self._nodes.select_empty()

    def select_enabled(self):
        return self._nodes.select_enabled()

    def select_file(self):
        return self._nodes.select_file()

    def select_first_child(self):
        return self._nodes.select_first_child()

    def select_nth_child(self, i):
        return self._nodes.select_nth_child(i)

    def select_nth_last_child(self, i):
        return self._nodes.select_nth_last_child(i)

    def select_last_child(self):
        return self._nodes.select_last_child()

    def select_first_of_type(self):
        return self._nodes.select_first_of_type()

    def select_last_of_type(self):
        return self._nodes.select_last_of_type()

    def select_nth_last_of_type(self, i):
        return self._nodes.select_nth_last_of_type(i)

    def select_nth_of_type(self, i):
        return self._nodes.select_nth_of_type(i)

    def select(self, attr):
        return self._nodes.select(attr)

    def select_has(self, pynodelist):
        return self._nodes.select_has(pynodelist)

    def select_image(self):
        return self._nodes.select_image()

    def select_input(self):
        return self._nodes.select_input()

    def select_lang(self, lang):
        return self._nodes.select_lang(lang)

    def select_attr(self, attr, value):
        return self._nodes.select_attr(attr, value)

    def select_attr_contains_prefix(self, attr, value):
        return self._nodes.select_attr_contains_prefix(attr, value)

    def select_attr_contains(self, attr, value):
        return self._nodes.select_attr_contains(attr, value)

    def select_attr_contains_word(self, attr, value):
        return self._nodes.select_attr_contains_word(attr, value)

    def select_attr_ends_with(self, attr, value):
        return self._nodes.select_attr_ends_with(attr, value)

    def select_attr_not_equal(self, attr, value):
        return self._nodes.select_attr_not_equal(attr, value)

    def select_attr_starts_with(self, attr, value):
        return self._nodes.select_attr_starts_with(attr, value)

    def select_only_child(self):
        return self._nodes.select_only_child()

    def select_only_of_type(self):
        return self._nodes.select_only_of_type()

    def select_parent(self):
        return self._nodes.select_parent()

    def select_password(self):
        return self._nodes.select_password()

    def select_radio(self):
        return self._nodes.select_radio()

    def select_reset(self):
        return self._nodes.select_reset()

    def select_root(self):
        return self._nodes.select_root()

    def select_selected(self):
        return self._nodes.select_selected()

    def select_submit(self):
        return self._nodes.select_submit()

    def select_text(self):
        return self._nodes.select_text()
