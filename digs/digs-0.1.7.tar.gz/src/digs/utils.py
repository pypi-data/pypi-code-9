#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-07-06 21:50:47
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-06 21:51:24
from kitchen.text.converters import to_unicode
from osinfo import osinfo

        

def to_display(s):
    s = s.strip()
    info = osinfo.OSInfo()
    if info == 'Windows':
        return to_unicode(s, 'utf-8')
    s = to_unicode(s)
    try:
        return s.encode('utf-8', 'replace')
    except Exception:
        pass
    return s