# lextab.py. This file automatically created by PLY (version 3.6). Don't edit!
_tabversion   = '3.5'
_lextokens    = set(['LSQUARE', 'RSQUARE', 'RPAREN', 'STRING', 'COMMA', 'LPAREN', 'INTEGER', 'DOT'])
_lexreflags   = 0
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_INTEGER>0|[1-9][0-9]*)|(?P<t_NEWLINE>\\n+)|(?P<t_STRING>\\w+)|(?P<t_LPAREN>\\()|(?P<t_RSQUARE>\\])|(?P<t_DOT>\\.)|(?P<t_RPAREN>\\))|(?P<t_LSQUARE>\\[)|(?P<t_COMMA>,)', [None, ('t_INTEGER', 'INTEGER'), ('t_NEWLINE', 'NEWLINE'), (None, 'STRING'), (None, 'LPAREN'), (None, 'RSQUARE'), (None, 'DOT'), (None, 'RPAREN'), (None, 'LSQUARE'), (None, 'COMMA')])]}
_lexstateignore = {'INITIAL': ' \t\n'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
