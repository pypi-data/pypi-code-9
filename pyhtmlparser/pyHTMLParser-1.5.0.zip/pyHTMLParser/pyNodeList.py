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

class pyNodeList(list):

    def __init__(self):
        super(self.__class__, self).__init__()

    def size(self):
        return len(self)

    def first(self):
        return self[0]

    def last(self):
        return self[-1]

    def eq(self, index):
        if len(self) > abs(index):
            return self[index]
        return None

    def even(self):
        ret = pyNodeList()
        is_even = False
        for node in self:
            if is_even: ret.append(node)
            is_even = not is_even
        return ret

    def odd(self):
        ret = pyNodeList()
        is_odd = True
        for node in self:
            if is_odd: ret.append(node)
            is_odd = not is_odd
        return ret

    def gt(self, index):
        return self[index:]

    def lt(self, index):
        return self[:index]

    def id(self, i):
        for node in self:
            if node.attr('id') == i:
                return node
        return None

    def cls(self, c):
        ret = pyNodeList()
        for node in self:
            n = node.attr('class')
            if n is not None and n.find(c) is not -1:
                ret.append(node)
        return ret

    def has_class(self, c):
        for node in self:
            n = node.attr('class')
            if n.find(c) is not -1:
                return True
        return False

    def contains(self, text):
        ret = pyNodeList()
        for node in self:
            if node.text().find(text) is not -1:
                ret.append(node)
        return ret

    def siblings(self):
        temp = pyNodeList()
        for node in self:
            brothers = node.siblings()
            if len(brothers) is not 0:
                temp.extend(brothers)
        ret = pyNodeList()
        ret.append(temp[0])
        for t in temp:
            for r in ret:
                if t != r:
                    ret.append(t)
        return ret
