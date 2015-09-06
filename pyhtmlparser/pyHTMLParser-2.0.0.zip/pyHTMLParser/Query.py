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

from pyHTMLParser.Parser import Parser
from pyHTMLParser.pyNode import pyNode, pyNodeList
import re

_parser = None
_ch = re.compile('[a-zA-Z0-9_\-]+')
_digit = re.compile('[0-9\-]+')

def _get_charactor(ch):
    global _ch
    ret = ''
    match = _ch.match(ch)
    while match is not None:
        ret += ch[0]
        ch = ch[1:]
        match = _ch.match(ch)
    return ret, ch

def is_pyNode(obj):
    return isinstance(obj, pyNode)

def is_pyNodeList(obj):
    return isinstance(obj, pyNodeList)

def _is_tag(selector):
    global _ch
    match = _ch.match(selector)
    return False if match is None else True

def _get_tag(tag, ancestor):
    global _parser
    if ancestor is not None and not is_pyNode(ancestor):
        return ancestor.tag(tag)
    elif ancestor is None:
        return _parser.tag(tag)
    else:
        return None

def _is_id(selector):
    return True if selector[0] == '#' else False

def _get_id(i, ancestor):
    global _parser
    if ancestor is not None and not is_pyNode(ancestor):
        return ancestor.id(i)
    elif ancestor is None:
        return _parser.id(i)
    else:
        return None

def _is_class(selector):
    return True if selector[0] == '.' else False

def _get_class(cls, ancestor):
    global _parser
    if ancestor is not None and not is_pyNode(ancestor):
        return ancestor.cls(cls)
    elif ancestor is None:
        return _parser.cls(cls)
    return None

def _is_space(selector):
    return True if selector[0] == ' ' else False

def _is_child_of(selector):
    return True if selector[0] == '>' else False

def _is_next_of(selector):
    return True if selector[0] == '+' else False

def _is_next_sibling_of(selector):
    return True if selector[0] == '~' else False

def _is_prev_of(selector):
    return True if selector[0] == '-' else False

def _is_prev_sibling_of(selector):
    return True if selector[0] == '<' else False

def _is_selectors(selector):
    if selector[0] == ':': return True
    elif selector[0] == '[' and selector.find(']') != -1:
        return True
    return False

def _is_colon(selector):
    if selector[0] == ':': return True
    return False

def _is_square_bracket(selector):
    if selector[0] == '[': return True
    return False

def _extract_selector(selector):
    selector = selector[1:]
    pos = selector.find(')')
    s = selector[:pos]
    return s, selector[pos + 1:]

def _is_equal(selector):
    return True if selector[0] == '=' else False

def _extract_value(value):
    if value[0] == '\'' and value[-1] == '\'' or \
       value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    return value

def _is_contains_prefix(value):
    e = re.compile('\|=')
    return True if e.match(value) is not None else False

def _is_attr_contains(value):
    e = re.compile('\*=')
    return True if e.match(value) is not None else False

def _is_attr_contains_word(value):
    e = re.compile('\~=')
    return True if e.match(value) is not None else False

def _is_ends_with(value):
    e = re.compile('\$=')
    return True if e.match(value) is not None else False

def _is_attr_not_equal(value):
    e = re.compile('\!=')
    return True if e.match(value) is not None else False

def _is_attr_starts_with(value):
    e = re.compile('\^=')
    return True if e.match(value) is not None else False


def Q_open(url, parser = None):
    global _parser
    if parser is not None:
        if _parser is not None:
            _parser.close()
            _parser.clear()
        _parser = parser
        _parser.open(url)
    else:
        if _parser is None:
            _parser = Parser()
            _parser.open(url)
        else:
            _parser.close()
            _parser.clear()
            _parser.open(url)
    _parser.construct()

def Q_close():
    global _parser
    if _parser is not None:
        _parser.close()
        _parser.clear()

def Q_html(html):
    global _parser
    if _parser is not None:
        _parser.close()
        _parser.clear()
        _parser.set_html(html)
        _parser.construct()

def Q(selector, ancestor = None):
    global _parser
    global _digit
    if selector == '': return ancestor
    ret = None
    p = None
    if ancestor is None: p = _parser
    else: p = ancestor
    if _is_space(selector):
        if ancestor is None: return None
        selector = selector.strip()
        if selector == '': return None
        symbols = ['>', '+', '-', '<']
        if selector[0] in symbols:
            symbol = selector[0]
            selector = selector[1:].strip()
            if symbol == '>':
                ret = Q(selector, ancestor.children())
            elif symbol == '+':
                ret = Q(selector, ancestor.select_next())
            elif symbol == '~':
                ret = Q(selector, ancestor.select_next_sibling())
            elif symbol == '-':
                ret = Q(selector, ancestor.select_prev())
            elif symbol == '<':
                ret = Q(selector, ancestor.select_prev_sibling())
        else:
            ret = Q(selector, ancestor.descendant())
    elif _is_tag(selector):
        tag, selector = _get_charactor(selector)
        if tag != '':
            ret = Q(selector, _get_tag(tag, ancestor))
    elif _is_id(selector):
        selector = selector[1:]
        _id, selector = _get_charactor(selector)
        if _id != '':
            ret = Q(selector, _get_id(_id, ancestor))
    elif _is_class(selector):
        selector = selector[1:]
        _class, selector = _get_charactor(selector)
        if _class != '':
            ret = Q(selector, _get_class(_class, ancestor))
    elif _is_child_of(selector):
        if ancestor is None: return None
        elif not ancestor.has_child(): return None
        selector = selector[1:].strip()
        if selector == '': return None
        ret = Q(selector, ancestor.children())
    elif _is_next_of(selector) or \
         _is_next_sibling_of(selector) or \
         _is_prev_of(selector) or \
         _is_prev_sibling_of(selector):
        if ancestor is None: return None
        selector = selector[1:].strip()
        if selector == '': return None
        if _is_next_of(selector):
            ret = Q(selector, ancestor.select_next())
        elif _is_next_sibling_of(selector):
            ret = Q(selector, ancestor.select_next_sibling())
        elif _is_prev_of(selector):
            ret = Q(selector, ancestor.select_prev())
        elif _is_prev_sibling_of(selector):
            ret = Q(selector, ancestor.select_prev_sibling())
    elif _is_selectors(selector):
        if _is_colon(selector):
            attr, selector = _get_charactor(selector[1:])
            selector = selector.strip()
            value = None
            if selector != '' and selector[0] == '(':
                value, selector = _extract_selector(selector)
                value = value.strip()
                if _digit.match(value) is not None:
                    value = int(value)
                    attrs = ['eq', 'gt', 'lt', 'nth-child', \
                             'nth-last-child', 'nth-last-of-type', \
                             'nth-of-type']
                    methods = ['eq', 'gt', 'lt', 'select_nth_child', \
                               'select_nth_last_child', 'select_nth_last_of_type', \
                               'select_nth_of_type']
                    for i in range(len(attrs)):
                        if attr == attrs[i]:
                            ret = Q(selector, p[methods[i]](value))
                else:
                    if attr == 'lang':
                        value = _extract_value(value)
                        ret = Q(selector, p.select_lang(value))
                    elif attr == 'contains':
                        value = _extract_value(value)
                        ret = Q(selector, p.contains(value))
                    else:
                        attrs = ['not', 'has']
                        methods = ['not_', 'select_has']
                        for i in range(len(attrs)):
                            if attr == attrs[i]:
                                ret = Q(selector, p[methods[i]](Q(value, None)))
            else:
                attrs = ['first', 'last', 'even', 'odd', 'button', \
                         'checkbox', 'checked', 'disabled', 'enabled', \
                         'file', 'first-child', 'last-child', \
                         'first-of-type', 'last-of-type', 'image', \
                         'input', 'header', 'only-child', 'only-of-type', \
                         'parent', 'password', 'radio', 'reset', \
                         'root', 'selected', 'submit', 'text']
                methods = ['first', 'last', 'even', 'odd', \
                           'select_button', 'select_checkbox', \
                           'select_checked', 'select_disabled', \
                           'select_enabled', 'select_file', \
                           'select_first_child', 'select_last_child', \
                           'select_first_of_type', 'select_last_of_type', \
                           'select_image', 'select_input', 'header', \
                           'select_only_child', 'select_only_of_type', \
                           'select_parent', 'select_password', \
                           'select_radio', 'select_reset', \
                           'select_root', 'select_selected', \
                           'select_submit', 'select_text']
                for i in range(len(attrs)):
                    if attr == attrs[i]:
                        ret = Q(selector, p[methods[i]]())
        elif _is_square_bracket(selector):
            attr, selector = _get_charactor(selector[1:])
            selector = selector.strip()
            pos = selector.find(']')
            value = selector[:pos]
            selector = selector[pos + 1:]
            if value == '':
                ret = Q(selector, p.select(attr))
            elif _is_equal(value):
                value = value[1:].strip()
                value = _extract_value(value)
                ret = Q(selector, p.select_attr(attr, value))
            else:
                v = value;
                value = value[2:].strip()
                value = _extract_value(value)
                conditions = [_is_contains_prefix, _is_attr_contains, \
                              _is_attr_contains_word, _is_ends_with, \
                              _is_attr_not_equal, _is_attr_starts_with]
                methods = ['select_attr_contains_prefix', 'select_attr_contains', \
                           'select_attr_contains_word', 'select_attr_ends_with', \
                           'select_attr_not_equal', 'select_attr_starts_with']
                for i in range(len(conditions)):
                    if conditions[i](v):
                        ret = Q(selector, p[methods[i]](attr, value))
    return ret
