# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

def escape(name):
    ret = u""
    for char in name:
        #Filenames starting with ".", zero-length space and division-slash require escaping
        if (char == u"." and ret == u"") or char in [u"\u200B", u"\u2215"]:
            ret += u"\u200B" + char
        #Slashes can only be used as folder separators. Use division-slash instead
        elif char == u"/":
            ret += u"\u2215"
        else:
            ret += char
    return ret
  

def unescape(name):
    ret = u""
    escaped = False
    for char in name:
        if escaped:
            ret += char
            escaped = False
        elif char == u"\u200B":
            escaped = True
        elif char == u"\u2215":
            ret += u"/"
        else:
            ret += char
    return ret