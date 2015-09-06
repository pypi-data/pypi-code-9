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

from pyHTMLParser.ParserUtils import is_self_closing
import re

class pyNodeList(list):

    def __init__(self):
        super(self.__class__, self).__init__()

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
        else:
            return super(self.__class__, self).__getitem__(fn)

    def size(self):
        return len(self)

    #Use:
    #  Q('li:first')
    #  Q('li').first()
    #Match:
    #  <ul>
    #    <li>match</li>
    #    <li>not match</li>
    #    <li>not match</li>
    #  </ul>
    def first(self):
        return self[0]

    #Use:
    #  Q('li:last')
    #  Q('li').last()
    #Match:
    #  <ul>
    #    <li>not match</li>
    #    <li>not match</li>
    #    <li>match</li>
    #  </ul>
    def last(self):
        return self[-1]

    #Use:
    #  Q('li:eq(3)')
    #  Q('li:eq(-3)')
    #  Q('li').eq(3)
    #Match:
    #  <ul>
    #    <li>not match</li>
    #    <li>not match</li>
    #    <li>not match</li>
    #    <li>match</li>
    #    <li>not match</li>
    #  </ul>
    def eq(self, index):
        if len(self) > abs(index):
            return self[index]
        return None

    #Use:
    #  Q('li:even')
    #  Q('li').even()
    #Match:
    #  <ul>
    #    <li>not match</li>
    #    <li>match</li>
    #    <li>not match</li>
    #    <li>match</li>
    #    <li>not match</li>
    #  </ul>
    def even(self):
        ret = pyNodeList()
        is_even = False
        for node in self:
            if is_even: ret.append(node)
            is_even = not is_even
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('li:odd')
    #  Q('li').odd()
    #Match:
    #  <ul>
    #    <li>match</li>
    #    <li>not match</li>
    #    <li>match</li>
    #    <li>not match</li>
    #    <li>match</li>
    #  </ul>
    def odd(self):
        ret = pyNodeList()
        is_odd = True
        for node in self:
            if is_odd: ret.append(node)
            is_odd = not is_odd
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('li:gt(2)')
    #  Q('li').gt(2)
    #Match:
    #  <ul>
    #    <li>not match</li>
    #    <li>not match</li>
    #    <li>not match</li>
    #    <li>match</li>
    #    <li>match</li>
    #  </ul>
    def gt(self, index):
        return self[index:]

    #Use:
    #  Q('li:lt(3)')
    #  Q('li').lt(3)
    #Match:
    #  <ul>
    #    <li>match</li>
    #    <li>match</li>
    #    <li>match</li>
    #    <li>not match</li>
    #    <li>not match</li>
    #  </ul>
    def lt(self, index):
        return self[:index]

    #Use:
    #  Q('div')
    #Match:
    #  <div></div>
    def tag(self, tag):
        t = tag.lower()
        ret = pyNodeList()
        for node in self:
            if node.name() == t:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('div#main')
    #  Q('#logo')
    #Match:
    #  <div id="main"></div>
    #  <img id="logo" src="****.png">
    def id(self, i):
        for node in self:
            if node.attr('id') == i:
                return node
        return None

    #Use
    #  Q('div.className')
    #  Q('.name')
    #Match:
    #  <div class="className"></div>
    #  <p class="name"></p>
    #  <span class="name"></span>
    def cls(self, c):
        ret = pyNodeList()
        cls_name = re.compile(c)
        for node in self:
            n = node.attr('class')
            if n is not None and cls_name.search(n) is not None:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def header(self):
        ret = pyNodeList()
        h = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        for node in self:
            if node.name() in h:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else return ret

    def has_cls(self, c):
        cls_name = re.compile(c)
        for node in self:
            n = node.attr('class')
            if n is not None and cls_name.search(n) is not None:
                return True
        return False

    def has_child(self):
        for node in self:
            if not node.has_child(): return False
        return True

    def children(self):
        ret = pyNodeList()
        for node in self:
            ch = node.children()
            if isinstance(ch, pyNodeList) and len(ch) != 0:
                ret.extend(ch)
            elif isinstance(ch, pyNode):
                ret.append(ch)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('div > a')
    #Match:
    #  <div>
    #    <a href="****.com">match</a>
    #    <p>Lorem ipsum <a href="++++.com">not match</a></p>
    #  </div>
    def child(self, child_tag = None):
        if child_tag is None: return self.children()
        ret = pyNodeList()
        for node in self:
            ch = node.child(child_tag)
            if isinstance(ch, pyNodeList) and len(ch) != 0:
                ret.extend(ch)
            elif isinstance(ch, pyNode):
                ret.append(ch)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('li:contains("item")')
    #Match:
    #  <li>item 1</li>
    #  <li>an item</li>
    #  <li>an itemized account</li>
    def contains(self, text):
        ret = pyNodeList()
        for node in self:
            if node.text().find(text) != -1:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def siblings(self):
        ret = pyNodeList()
        for node in self:
            brothers = node.siblings()
            if isinstance(brothers, pyNodeList) and len(brothers) != 0:
                for bro in brothers:
                    duplicated = False
                    if len(ret) != 0:
                        for r in ret:
                            if bro == r:
                                duplicated = True
                                break
                    if not duplicated: ret.append(bro)
            elif isinstance(brothers, pyNode):
                duplicated = True
                if len(ret) != 0:
                    for r in ret:
                        if brothers == r:
                            duplicated = True
                            break
                if not duplicated: ret.append(brothers)
        if len(ret) == 1: return ret[0]
        else: return ret

    def descendant(self):
        ret = pyNodeList()
        for node in self:
            d = node.descendant()
            if isinstance(d, pyNodeList) and len(d) != 0:
                ret.extend(d)
            elif isinstance(d, pyNode):
                ret.append(d)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('div li')
    #  Q('div ul li')
    def descendant_tag(self, tag):
        t = tag.lower()
        ret = pyNodeList()
        for node in self:
            descendant = node.descendant_tag(t)
            if isinstance(descendnat, pyNodeList) and len(descendant) != 0:
                ret.extend(descendant)
            elif isinstance(descendant, pyNode):
                ret.append(descendant)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('div .className')
    #  Q('ul .list .link')
    def descendant_cls(self, cls):
        ret = pyNodeList()
        for node in self:
            descendant = node.descendant_class(cls)
            if isinstance(descendant, pyNodeList) and len(descendant) != 0:
                ret.extend(descendant)
            elif isinstance(descendant, pyNode):
                ret.append(descendant)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('input:not(:checked)')
    #  Q('a:not(.link)')
    #  Q('div:not(#main)')
    #  Q('p:not(ul li > p)')
    #Match:
    #  <input type="checkbox">
    #  <a class="notLink" href="****.com">not link</a>
    #  <div id="notMain">not main</div>
    #  <div><p>not child of li</p></div>
    def not_(self, pynodelist):
        ret = pyNodeList()
        for node in self:
            dif = True
            for another in pynodelist:
                if node == another:
                    dif = False
                    break
            if dif:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q(':button')
    #  Q('input:button')
    #Match:
    #  <button>Button</button>
    #  <input type="button">
    def select_button(self):
        ret = pyNodeList()
        for node in self:
            if node.name() == 'button':
                ret.append(node)
            else:
                t = node.attr('type')
                if t is not None and t.lower() == 'button':
                    ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q(':checkbox')
    #  Q('input:checkbox')
    #Match:
    #  <input type="checkbox">
    def select_checkbox(self):
        ret = pyNodeList()
        for node in self:
            t = node.attr('type')
            if t is not None and t.lower() == 'checkbox':
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q(':checked')
    #  Q('input:checked')
    #Match:
    #  <input type="****" checked="checked">
    #  <input type="++++" checked>
    def select_checked(self):
        ret = pyNodeList()
        for node in self:
            t = node.attr('checked')
            if t is not None:
                if t.lower() == 'checked' or t == '':
                    ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q(':disabled')
    #  Q('input:disabled')
    #Match:
    #  <input type="****" disabled="disabled">
    #  <input type="++++" disabled>
    def select_disabled(self):
        ret = pyNodeList()
        tags = ['button', 'input', 'optgroup', 'option', 'select', 'textarea']
        for node in self:
            if node.name() in tags:
                t = node.attr('disabled')
                if t is not None:
                    if t == 'disabled' or t == '':
                        ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('li:empty')
    #Match:
    #  <li></li>
    #  <li><a href="****.com"></a></li>
    def select_empty(self):
        ret = pyNodeList()
        for node in self:
            if node.name() != 'comment':
                if node.text() == '':
                    ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('input:enabled')
    #Match:
    #  <input type="****">
    #  <input type="++++">
    def select_enabled(self):
        ret = pyNodeList()
        tags = ['button', 'input', 'optgroup', 'option', 'select', 'textarea']
        for node in self:
            if node.name() in tags:
                t = node.attr('disabled')
                if t is None:
                    ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('input:file')
    #Match:
    #  <input type="file">
    def select_file(self):
        ret = pyNodeList()
        for node in self:
            t = node.attr('type')
            if t is not None and t.lower() == 'file':
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('ul li:first-child')
    #Match:
    #  <ul>
    #    <li>match</li>
    #    <li>not match</li>
    #    <li>not match</li>
    #  </ul>
    def select_first_child(self):
        parents = list()
        ret = pyNodeList()
        tag = self[0].name()
        for node in self:
            duplicated = False
            if len(parents) != 0:
                for p in parents:
                    if p == node.parent():
                        duplicated = True
                        break
            if not duplicated: parents.append(node.parent())
            if tag != node.name():
                return pyNodeList()
        if len(parents) != 0:
            for parent in parents:
                n = parent.child(tag)
                if isinstance(n, pyNodeList) and len(n) != 0: n = n.first()
                if n is not None: ret.append(n)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('ul li:nth-child(2)')
    #Match:
    #  <ul>
    #    <li>not match</li>
    #    <li>match</li>
    #    <li>not match</li>
    #  </ul>
    def select_nth_child(self, i):
        index = i - 1
        parents = list()
        ret = pyNodeList()
        tag = self[0].name()
        for node in self:
            duplicated = False
            if len(parents) != 0:
                for p in parents:
                    if p == node.parent():
                        duplicated = True
                        break
            if not duplicated: parents.append(node.parent())
            if tag != node.name():
                return pyNodeList()
        if len(parents) != 0:
            for parent in parents:
                n = parent.child(tag)
                if isinstance(n, pyNodeList) and len(n) != 0: n = n.eq(index)
                if n is not None: ret.append(n)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('ul li:nth-last-child(2)')
    #Match:
    #  <ul>
    #    <li>not match</li>
    #    <li>not match</li>
    #    <li>match</li>
    #    <li>not match</li>
    #  </ul>
    def select_nth_last_child(self, i):
        parents = list()
        ret = pyNodeList()
        tag = self[0].name()
        for node in self:
            duplicated = False
            if len(parents) != 0:
                for p in parents:
                    if p == node.parent():
                        duplicated = True
                        break
            if not duplicated: parents.append(node.parent())
            if tag != node.name():
                return pyNodeList()
        if len(parents) != 0:
            for parent in parents:
                ch = parent.child(tag)
                if isinstance(ch, pyNodeList) and len(ch) != 0:
                    n = ch.eq(-1 * i)
                    if n is not None: ret.append(n)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('ul li:last-child')
    #Match:
    #  <ul>
    #    <li>not match</li>
    #    <li>not match</li>
    #    <li>not match</li>
    #    <li>match</li>
    #  </ul>
    def select_last_child(self):
        parents = list()
        tag = self[0].name()
        for node in self:
            duplicated = False
            if len(parents) != 0:
                for p in parents:
                    if p == node.parent():
                        duplicated = True
                        break
            if not duplicated: parents.append(node.parent())
        ret = pyNodeList()
        if len(parents) != 0:
            for parent in parents:
                n = parent.child(tag)
                if isinstance(n, pyNodeList) and len(n) != 0: n = n.last()
                if n is not None: ret.append(n)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('li:first-of-type')
    #Match:
    #  <ul>
    #    <li>match</li>
    #    <li>not match</li>
    #    <li>
    #      <ul>
    #        <li>match</li>
    #        <li>not match</li>
    #        <li>not match</li>
    #      </ul>
    #    </li>
    #    <li>not match</li>
    #  </ul>
    def select_first_of_type(self):
        parents = list()
        tag = self[0].name()
        for node in self:
            duplicated = False
            if len(parents) != 0:
                for p in parents:
                    if p == node.parent():
                        duplicated = True
                        break
            if not duplicated: parents.append(node.parent())
        ret = pyNodeList()
        if len(parents) != 0:
            for parent in parents:
                n = parent.child(tag)
                if isinstance(n, pyNodeList) and len(n) != 0: n = n.first()
                if n is not None: ret.append(n)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('li:last-of-type')
    #Match:
    #  <ul>
    #    <li>not match</li>
    #    <li>not match</li>
    #    <li>
    #      <ul>
    #        <li>not match</li>
    #        <li>not match</li>
    #        <li>match</li>
    #      </ul>
    #    </li>
    #    <li>match</li>
    #  </ul>
    def select_last_of_type(self):
        parents = list()
        ret = pyNodeList()
        tag = self[0].name()
        for node in self:
            duplicated = False
            if len(parents) != 0:
                for p in parents:
                    if p == node.parent():
                        duplicated = True
                        break
            if not duplicated: parents.append(node.parent())
            if tag != node.name():
                return ret
        if len(parents) != 0:
            for parent in parents:
                n = parent.child(tag)
                if isinstance(n, pyNodeList) and len(n) != 0: n = n.last()
                if n is not None: ret.append(n)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('li:nth-last-of-type(2)')
    #Match:
    #  <ul>
    #    <li>not match</li>
    #    <li>not match</li>
    #    <li>
    #      <ul>
    #        <li>not match</li>
    #        <li>not match</li>
    #        <li>match</li>
    #        <li>not match</li>
    #      </ul>
    #    </li>
    #    <li>match</li>
    #    <li>not match</li>
    #  </ul>
    def select_nth_last_of_type(self, i):
        parents = list()
        ret = pyNodeList()
        tag = self[0].name()
        for node in self:
            duplicated = False
            if len(parents) != 0:
                for p in parents:
                    if p == node.parent():
                        duplicated = True
                        break
            if not duplicated: parents.append(node.parent())
            if tag != node.name():
                return ret
        ret = pyNodeList()
        if len(parents) != 0:
            for parent in parents:
                ch = parent.child(tag)
                if isinstance(ch, pyNodeList) and len(ch) != 0:
                    n = ch.eq(-1 * i)
                    if n is not None: ret.append(n)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('ul li:nth-of-type(2)')
    #Match:
    #  <ul>
    #    <li>not match</li>
    #    <li>match</li>
    #    <li>
    #      <ul>
    #        <li>not match</li>
    #        <li>match</li>
    #        <li>not match</li>
    #        <li>not match</li>
    #      </ul>
    #    </li>
    #    <li>not match</li>
    #    <li>not match</li>
    #  </ul>
    def select_nth_of_type(self, i):
        parents = list()
        ret = pyNodeList()
        tag = self[0].name()
        for node in self:
            duplicated = False
            if len(parents) != 0:
                for p in parents:
                    if p == node.parent():
                        duplicated = True
                        break
            if not duplicated: parents.append(node.parent())
            if tag != node.name():
                return ret
        ret = pyNodeList()
        if len(parents) != 0:
            for parent in parents:
                ch = parent.child(tag)
                if isinstance(ch, pyNodeList) and len(ch) != 0:
                    n = ch.eq(i - 1)
                    if n is not None: ret.append(n)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('[id]')
    #Match:
    #  <div id="main"></div>
    #  <img id="logo">
    def select(self, attr):
        ret = pyNodeList()
        for node in self:
            a = node.attr(attr)
            if a is not None:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('div:has(p)')
    #  Q('div:has(.link)')
    #  Q('div:has(#logo)')
    #  Q('form:has(:button)')
    #Match:
    #  <div><p></p></div>
    #  <div><ul><li><p></p></li></ul></div>
    #  <div><a href="****.com" class="link">link</a></div>
    #  <div><img id="logo" src="****.png"></div>
    #  <form><input type="button"></form>
    def select_has(self, pynodelist):
        ret = pyNodeList()
        for node in self:
            descendant = node.descendant()
            if isinstance(descendant, pyNode):
                for another in pynodelist:
                    if descendant == another:
                        ret.append(node)
            elif isinstance(descendant, pyNodeList) and len(descendant) != 0:
                for d in descendant:
                    for another in pynodelist:
                        if d == another:
                            ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('input:image')
    #  Q(':image')
    #Match:
    #  <input type="image">
    def select_image(self):
        ret = pyNodeList()
        for node in self:
            t = node.attr('type')
            if t is not None and t.lower() == 'image':
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q(':input')
    #Match:
    #  <input type="*">
    def select_input(self):
        ret = pyNodeList()
        for node in self:
            if node.name() == 'input':
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('div:lang("en-us")')
    #  Q('div:lang(en-us)')
    #Match:
    #  <div lang="en-us"></div>
    def select_lang(self, lang):
        ret = pyNodeList()
        for node in self:
            l = node.attr('lang')
            if l is not None and l == lang:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret
    #Use:
    #  Q('input[type="button"]')
    #  Q('input[type=button]')
    #Match:
    #  <input type="button">
    def select_attr(self, attr, value):
        ret = pyNodeList()
        for node in self:
            a = node.attr(attr)
            if a is not None and a == value:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('div + span')
    #Match:
    #  <div></div>
    #  <span>match</span>
    #  <span>not match</span>
    def select_next(self):
        ret = pyNodeList()
        for node in self:
            n = node.next_element()
            if n is not None:
                duplicated = False
                if len(ret) != 0:
                    for r in ret:
                        if r == n:
                            duplicated = True
                            break
                if not duplicated: ret.append(n)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('div ~ span')
    #Match:
    #  <div><span>not match</span></div>
    #  <span>match</span>
    #  <span>match</span>
    def select_next_sibling(self):
        ret = pyNodeList()
        for node in self:
            n = node.next_all()
            if isinstance(n, pyNode):
                duplicated = False
                if len(ret) != 0:
                    for r in ret:
                        if r == n:
                            duplicated = True
                            break
                if not duplicated: ret.append(n)
            elif isinstance(n, pyNodeList) and len(n) != 0:
                for elem in n:
                    duplicated = False
                    if len(ret) != 0:
                        for r in ret:
                            if r == elem:
                                duplicated = True
                                break
                    if not duplicated: ret.append(elem)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('div - span')
    #Match:
    #  <span>not match</span>
    #  <span>match</span>
    #  <div></div>
    #  <span>not match</span>
    #  <span>not match</span>
    def select_prev(self):
        ret = pyNodeList()
        for node in self:
            p = node.prev_element()
            if p is not None:
                duplicated = False
                if len(ret) != 0:
                    for r in ret:
                        if r == p:
                            duplicated = True
                            break
                if not duplicated: ret.append(p)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('div < span')
    #Match:
    #  <span>match</span>
    #  <span>match</span>
    #  <div></div>
    #  <span>not match</span>
    #  <span>not match</span>
    def select_prev_sibling(self):
        ret = pyNodeList()
        for node in self:
            n = node.prev_all()
            if isinstance(n, pyNode):
                duplicated = False
                if len(ret) != 0:
                    for r in ret:
                        if r == n:
                            duplicated = True
                            break
                if not duplicated: ret.append(n)
            else:
                for elem in n:
                    duplicated = False
                    if len(ret) != 0:
                        for r in ret:
                            if r == elem:
                                duplicated = True
                                break
                    if not duplicated: ret.append(elem)
        if len(ret) == 1: return ret[0]
        else: return ret
    
    #Use:
    #  Q('p[lang|="en"])
    #  Q('p[lang|=en])
    #Match:
    #  <p lang="en"></p>
    #  <p lang="en-*"></p>
    def select_attr_contains_prefix(self, attr, value):
        ret = pyNodeList()
        for node in self:
            if node.attr_contains_prefix(attr, value):
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('input[name*="man"]')
    #  Q('input[name*=man]')
    #Match:
    #  <input name="manual">
    #  <input name="chocolateman">
    #  <input name="germany">
    def select_attr_contains(self, attr, value):
        ret = pyNodeList()
        for node in self:
            if node.attr_contains(attr, value):
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('input[name~="man"])
    #  Q('input[name~=man])
    #Match:
    #  <input name="man eater">
    #  <input name="chocolate man">
    def select_attr_contains_word(self, attr, value):
        ret = pyNodeList()
        for node in self:
            if node.attr_contains_word(attr, value):
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('input[name$="letter"])
    #  Q('input[name$=letter])
    #Match:
    #  <input name="businessletter">
    #  <input name="newsletter">
    def select_attr_ends_with(self, attr, value):
        ret = pyNodeList()
        for node in self:
            if node.attr_ends_with(attr, value):
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('img[alt!="icon"]')
    #  Q('img[alt!=icon]')
    #Match:
    #  <img src="***.png" alt="background">
    #  <img src="+++.png" alt="logo">
    def select_attr_not_equal(self, attr, value):
        ret = pyNodeList()
        for node in self:
            a = node.attr(attr)
            if a is None or a != value:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    #Use:
    #  Q('input[name^="man"]')
    #  Q('input[name^=man]')
    #Match:
    #  <input name="many">
    #  <input name="manual">
    def select_attr_starts_with(self, attr, value):
        ret = pyNodeList()
        for node in self:
            if node.attr_starts_with(attr, value):
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def select_only_child(self):
        ret = pyNodeList()
        for node in self:
            if node.has_parent():
                if len(node.parent().children()) == 1:
                    ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def select_only_of_type(self):
        ret = pyNodeList()
        for node in self:
            if node.has_parent():
                tag_name = node.name()
                duplicated = False
                for ch in node.parent().children():
                    if ch != node and tag_name == ch.name():
                        duplicated = True
                        break
                if not duplicated: ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def select_parent(self):
        ret = pyNodeList()
        for node in self:
            if len(node.children()) != 0 or len(node.text()) != 0:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def select_password(self):
        ret = pyNodeList()
        for node in self:
            t = node.attr('type')
            if t is not None and t.lower() == 'password':
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def select_radio(self):
        ret = pyNodeList()
        for node in self:
            t = node.attr('type')
            if t is not None and t.lower() == 'radio':
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def select_reset(self):
        ret = pyNodeList()
        for node in self:
            t = node.attr('type')
            if t is not None and t.lower() == 'reset':
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def select_root(self):
        return self.tag('html')

    def select_selected(self):
        ret = pyNodeList()
        for node in self:
            if node.name() == 'option':
                s = node.attr('selected')
                if s is not None and (s.lower() == 'selected' or s == ''):
                    ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def select_submit(self):
        ret = pyNodeList()
        for node in self:
            t = node.attr('type')
            if t is not None and t.lower() == 'submit':
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def select_text(self):
        ret = pyNodeList()
        for node in self:
            t = node.attr('type')
            if t is not None and t.lower() == 'text':
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

class pyNode:

    def __init__(self, name=None):
        self._name = name
        self._attr = {}
        self._html = ''
        self._text = ''
        self._comment = []
        self._parent = None
        self._children = pyNodeList()

    def __str__(self):
        return self._name

    def __eq__(self, node):
        if self._name == node._name and \
           self._attr == node._attr and \
           self._html == node._html and \
           self._parent == node._parent:
            return True
        return False

    def __ne__(self, node):
        return not self.__eq__(node)

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def is_null(self):
        return True if self._name is None else False

    def set_attr(self, key, value):
        if not key in self._attr: self._attr[key] = value
        else: self._attr[key] += ' ' + value

    def attr(self, key):
        if not key in self._attr: return None
        else: return self._attr[key]

    def id(self):
        return self._attr['id'] if 'id' in self._attr else None

    def cls(self):
        if 'class' in self._attr: return self._attr['class']
        else: return None

    def has_cls(self, cls):
        if 'class' in self._attr:
            cls_name = re.compile(cls)
            if cls_name.search(self._attr['class']) is not None:
                return True
        return False

    def html(self):
        if self._name != 'comment':
            if self._html != '': return self._html
            self._html += '<' + self.name()
            for attr in self._attr:
                a = self._attr[attr]
                if a is not None:
                    self._html += ' ' + attr + '="' + self._attr[attr] + '"'
            self._html += '>' + self._text
            if not is_self_closing(self.name()):
                if self.has_child:
                    for ch in self._children:
                        self._html += ch.html()
                self._html += '</' + self.name() + '>'
            return self._html
        else:
            return self.comment()

    def set_html(self, html):
        self._html = html

    def text(self):
        if self._name != 'comment':
            ret = self._text
            if self.has_child():
                for child in self._children:
                    if ret != '':
                        ret += ' ' + child.text()
                    else:
                        ret += child.text()
            return ret
        else:
            return self.comment()

    def set_text(self, text):
        self._text = text

    def add_text(self, text):
        self._text += text

    def comment(self):
        ret = []
        for comment in self._comment:
            com = '<!--' + comment + '-->'
            ret.append(com)
        return ' '.join(ret)

    def add_comment(self, comment):
        self._comment.append(comment)

    def has_parent(self):
        return False if self._parent is None else True

    def set_parent(self, parent):
        self._parent = parent

    def parent(self):
        return self._parent

    def ancestor(self):
        if self.has_parent():
            ret = pyNodeList()
            par = self._parent
            ret.append(par)
            while par.has_parent():
                par = par._parent
                ret.append(par)
            if len(ret) == 1: return ret[0]
            else: return ret
        return None

    def has_child(self):
        return len(self._children) != 0

    def add_child(self, child):
        self._children.append(child)

    def children(self):
        ret = pyNodeList()
        for child in self._children:
            if child.name() != 'comment':
                ret.append(child)
        if len(ret) == 1: return ret[0]
        else: return ret

    def child(self, child_tag = None):
        if child_tag is None: return self.children()
        ret = pyNodeList()
        for node in self._children:
            if node.name() == child_tag:
                ret.append(node)
        if len(ret) == 1: return ret[0]
        else: return ret

    def next_all(self):
        ret = pyNodeList()
        if self.has_parent():
            brothers = self._parent.children()
            if isinstance(brothers, pyNodeList) and len(brothers) != 0:
                passed = False
                for bro in brothers:
                    if bro.name() != 'comment':
                        if passed: ret.append(bro)
                        if not passed and bro == self: passed = True
        if len(ret) == 1: return ret[0]
        else: return ret

    def prev_all(self):
        ret = pyNodeList()
        if self.has_parent():
            brothers = self._parent.children()
            if isinstance(brothers, pyNodeList) and len(brothers) != 0:
                for bro in brothers:
                    if bro.name() != 'comment':
                        if bro == self: break
                        ret.append(bro)
            elif isinstance(brothers, pyNode):
                ret.append(brothers)
        if len(ret) == 1: return ret[0]
        else: return ret

    def siblings(self):
        ret = pyNodeList()
        if self.has_parent():
            children = self._parent.children()
            if isinstance(children, pyNodeList) and len(children) != 0:
                for ch in children:
                    if self != ch:
                        ret.append(ch)
            elif isinstance(children, pyNodeList):
                ret.append(children)
        if len(ret) == 1: return ret[0]
        else: return ret

    def descendant(self):
        ret = pyNodeList()
        if self.has_child():
            children = self.children()
            if isinstance(children, pyNodeList) and len(children) != 0:
                for ch in children:
                    ret.append(ch)
                    grand = ch.descendant()
                    if isinstance(grand, pyNodeList) and len(grand) != 0:
                        ret.extend(grand)
                    elif isinstance(grand, pyNode):
                        ret.append(grand)
            elif isinstance(children, pyNode):
                ret.append(children)
                grand = children.descendant()
                if isinstance(grand, pyNodeList) and len(grand) != 0:
                    ret.extend(grand)
                elif isinstance(grand, pyNode):
                    ret.append(grand)
        if len(ret) == 1: return ret[0]
        else: return ret

    def descendant_tag(self, tag):
        t = tag.lower()
        ret = pyNodeList()
        if self.has_child():
            children = self.children()
            if isinstance(children, pyNodeList) and len(children) != 0:
                for ch in children:
                    if ch.name() == t:
                        ret.append(ch)
                    descendant = ch.descendant_tag(t)
                    if isinstance(descendant, pyNodeList) and len(descendant) != 0:
                        ret.extend(descendant)
                    elif isinstance(descendant, pyNode):
                        ret.append(descendant)
            elif isinstance(children, pyNode):
                if children.name() == t:
                    ret.append(children)
                descendant = children.descendant_tag(t)
                if isinstance(descendant, pyNodeList) and len(descendant) != 0:
                    ret.extend(descendant)
                elif isinstance(descendant, pyNode):
                    ret.append(descendant)
        if len(ret) == 1: return ret[0]
        else: return ret

    def descendant_cls(self, cls):
        ret = pyNodeList()
        cls_name = re.compile(cls)
        if self.has_child():
            children = self.children()
            if isinstance(children, pyNodeList) and len(children) != 0:
                for ch in children:
                    c = ch.attr('class')
                    if c is not None and cls_name.search(c) is not None:
                        ret.append(ch)
                    descendant = ch.descendant_cls(cls)
                    if isinstance(descendant, pyNodeList) and len(descendant) != 0:
                        ret.extend(descendant)
                    elif isinstance(descendant, pyNode):
                        ret.append(descendant)
            elif isinstance(children, pyNode):
                c = children.attr('class')
                if c is not None and cls_name.search(c) is not None:
                    ret.append(children)
                descendant = children.descendant_cls(cls)
                if isinstance(descendant, pyNodeList) and len(descendant) != 0:
                    ret.extend(descendant)
                elif isinstance(descendant, pyNode):
                    ret.append(descendant)
        if len(ret) == 1: return ret[0]
        else: return ret

    def next_element(self):
        if self.has_parent():
            brothers = self._parent.children()
            if isinstance(brothers, pyNodeList) and len(brothers) != 0:
                passed = False
                for bro in brothers:
                    if bro.name() != 'comment':
                        if passed: return bro
                        if not passed and bro == self: passed = True
        return None

    def prev_element(self):
        if self.has_parent():
            brothers = self._parent.children()
            if isinstance(brothers, pyNodeList) and len(brothers) != 0:
                for i in range(len(brothers)):
                    if brothers[i].name() != 'comment':
                        if brothers[i] == self and i != 0:
                            return brothers[i - 1]
        return None

    def attr_contains_prefix(self, attr, value):
        a = self.attr(attr)
        if a is not None:
            if a.find(value) == 0 and a[len(value)] == '-':
                return True
        return False
            
    def attr_contains(self, attr, value):
        a = self.attr(attr)
        if a is not None:
            if a.find(value) != -1:
                return True
        return False

    def attr_contains_word(self, attr, value):
        a = self.attr(attr)
        if a is not None:
            val = re.compile(value)
            if val.search(a) is not None:
                return True
        return False

    def attr_ends_with(self, attr, value):
        a = self.attr(attr)
        if a is not None:
            ends = re.compile(value + '$')
            if ends.search(a) is not None:
                return True
        return False

    def attr_starts_with(self, attr, value):
        a = self.attr(attr)
        if a is not None:
            starts = re.compile(value)
            if starts.match(a) is not None:
                return True
        return False

    def select_next(self):
        return self.next_element()

    def select_next_sibling(self):
        ret = pyNodeList()
        n = self.next_all()
        if isinstance(n, pyNode):
            ret.append(n)
        elif isinstance(n, pyNodeList) and len(n) != 0:
            for elem in n:
                ret.append(elem)
        if len(ret) == 1: return ret[0]
        else: return ret

    def select_prev(self):
        return self.prev_element()

    def select_prev_sibling(self):
        ret = pyNodeList()
        n = self.prev_all()
        if isinstance(n, pyNode):
            ret.append(n)
        else:
            for elem in n:
                ret.append(elem)
        if len(ret) == 1: return ret[0]
        else: return ret
