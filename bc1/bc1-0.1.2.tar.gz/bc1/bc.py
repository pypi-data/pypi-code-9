from .pyflex import lex as lex
from .pyflex import yacc as yacc

__author__ = 'jpercent'


class BC(object):
    def __init__(self, expression=None):
        super(BC, self).__init__()
        if not expression:
            self.fn = self.repl
        else:
            self.fn = lambda x: x.parse(expression)

    def parse(self, expression=None):

        tokens = (
            'NAME','NUMBER',
            'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
            'LPAREN','RPAREN',
            )

        t_PLUS    = r'\+'
        t_MINUS   = r'-'
        t_TIMES   = r'\*'
        t_DIVIDE  = r'/'
        t_EQUALS  = r'='
        t_LPAREN  = r'\('
        t_RPAREN  = r'\)'
        t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

        def t_NUMBER(t):
            r'\d+'
            try:
                t.value = int(t.value)
            except ValueError:
                print("Integer value error %d", t.value)
                t.value = 0
            return t

        t_ignore = " \t"

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += t.value.count("\n")

        def t_error(t):
            print("Unsupported character '%s'" % t.value[0])
            t.lexer.skip(1)

        # Build the lexer
        lexer = lex.lex()

        # Parsing rules

        precedence = (
            ('left','PLUS','MINUS'),
            ('left','TIMES','DIVIDE'),
            ('right','UMINUS'),
            )

        # dictionary of names
        names = { }

        def p_statement_expr(t):
            'statement : expression'
            print(t[1])

        def p_expression_binop(t):
            '''expression : expression PLUS expression
                          | expression MINUS expression
                          | expression TIMES expression
                          | expression DIVIDE expression'''
            if t[2] == '+'  : t[0] = int(t[1] + t[3])
            elif t[2] == '-': t[0] = int(t[1] - t[3])
            elif t[2] == '*': t[0] = int(t[1] * t[3])
            elif t[2] == '/': t[0] = int(t[1] / t[3])

        def p_expression_uminus(t):
            'expression : MINUS expression %prec UMINUS'
            t[0] = -t[2]

        def p_expression_group(t):
            'expression : LPAREN expression RPAREN'
            t[0] = t[2]

        def p_expression_number(t):
            'expression : NUMBER'
            t[0] = t[1]

        def p_expression_name(t):
            'expression : NAME'
            try:
                t[0] = names[t[1]]
            except LookupError:
                print("Undefined name '%s'" % t[1])
                t[0] = 0

        def p_error(t):
            if t:
                print("Syntax error at '%s'" % t.value)

        self.fn(yacc.yacc())

    def repl(self, parser):
        print("bc .1")
        print("Copyright 2015 Syndetic Logic, LLC")
        print("All rights reserved")
        while True:
            try:
                s = input('>')   # Use raw_input on Python 2
            except EOFError:
                break
            parser.parse(s)






