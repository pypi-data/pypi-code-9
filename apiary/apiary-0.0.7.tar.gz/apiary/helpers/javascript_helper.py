# -*- coding: utf-8 -*-
import re
from pprint import pprint

JS_ESCAPE_MAP = {
    '\\': '\\\\',
    '</': '<\\/',
    "\r\n": "\\n",
    "\n": "\\n",
    "\r": "\n",
    '"': '\\"',
    "'": "\\'",
    "\342\200\250": '&#x2028;',
    "\342\200\251": '&#x2029;'
}


def match(m):
    pprint(m.group())
    return JS_ESCAPE_MAP[m.group()]


def escape_javascript(javascript):
    if javascript:
        return re.sub(r"(\\|</|\r\n|\342\200\250|\342\200\251|[\n\r\"\'])", match, javascript)
    else:
        ''
