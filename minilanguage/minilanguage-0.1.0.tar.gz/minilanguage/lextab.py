# lextab.py. This file automatically created by PLY (version 3.6). Don't edit!
_tabversion   = '3.5'
_lextokens    = set(['COMMENT', 'AND', 'GT', 'RPAREN', 'GTE', 'NOT_EQUALS', 'LTE', 'HEX', 'NUMBER', 'OR', 'EQUALS', 'LT', 'LPAREN', 'IN', 'NOT', 'FALSE', 'TRUE', 'ID', 'DOT', 'STRING'])
_lexreflags   = 0
_lexliterals  = '+-*/'
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_HEX>0x[0-9a-fA-F]+)|(?P<t_NUMBER>\\d+)|(?P<t_COMMENT>\\#.*)|(?P<t_DOT>\\.)|(?P<t_TRUE>True)|(?P<t_FALSE>False)|(?P<t_STRING>(?P<quote>[\'\\"]).*?(?P=quote))|(?P<t_ID>[a-zA-Z_][a-zA-Z_0-9]*)|(?P<t_newline>\\n+)|(?P<t_NOT_EQUALS>!=)|(?P<t_GTE>>=)|(?P<t_LPAREN>\\()|(?P<t_LTE><=)|(?P<t_EQUALS>==)|(?P<t_RPAREN>\\))|(?P<t_LT><)|(?P<t_GT>>)', [None, ('t_HEX', 'HEX'), ('t_NUMBER', 'NUMBER'), ('t_COMMENT', 'COMMENT'), ('t_DOT', 'DOT'), ('t_TRUE', 'TRUE'), ('t_FALSE', 'FALSE'), ('t_STRING', 'STRING'), None, ('t_ID', 'ID'), ('t_newline', 'newline'), (None, 'NOT_EQUALS'), (None, 'GTE'), (None, 'LPAREN'), (None, 'LTE'), (None, 'EQUALS'), (None, 'RPAREN'), (None, 'LT'), (None, 'GT')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
