# -*- coding: utf-8 -*-
import re

RE_MIXINS_FIND = r'\.([\w\-]*)\s*\((.*)\)\s*\{'
RE_MIXINS_REPLACE = r'@mixin \1\(\2\)\n{'
RE_INCLUDE_FIND = r'\.([\w\-]*\(.*\)\s*;)'
RE_INCLUDE_REPLACE = r'@include \1'
RE_STRING_LITERALS_FIND = r'~"(.*)"'
RE_STRING_LITERALS_REPLACE = r'#{"\1"}'

RE = {
    'identifiers': {
        'pattern': r'@(?!font-face|import|media|keyframes|-)',
        'repl': r'$',
    },
    'mixins_dynamic': {
        'pattern': r'\.([\w\-]*)\s*\((.*)\)\s*\{',
        'repl': r'@mixin \1(\2) {',
    },
    'mixins': {
        'pattern': r'\.([\w\-]*)\s*\{',
        'repl': r'@mixin \1 {',
    },
    'include_dynamic': {
        'pattern': r'\.([\w\-]*\(.*\)\s*;)',
        'repl': r'@include \1',
    },
    'include': {
        'pattern': r'\.([\w\-]*\s*;)',
        'repl': r'@include \1',
    },
    'string_literals': {
        'pattern': r'~"(.*)"',
        'repl': r'#{"\1"}',
    },
}


def replace_identifiers(string):
    """ Run first, replaces @'s with $'s """
    return re.sub(string=string, **RE['identifiers'])


def replace_mixins(string):
    string = re.sub(string=string, **RE['include_dynamic'])
    string = re.sub(string=string, **RE['include'])
    string = re.sub(string=string, **RE['mixins_dynamic'])
    return re.sub(string=string, **RE['mixins'])


def replace_string_leterals(string):
    return re.sub(string=string, **RE['string_literals'])

def convert(string):
    string = replace_identifiers(string)
    string = replace_mixins(string)
    string = replace_string_leterals(string)
    return string

