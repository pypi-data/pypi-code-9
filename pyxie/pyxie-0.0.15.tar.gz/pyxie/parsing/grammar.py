#!/usr/bin/python
#
# Copyright 2015 Michael Sparks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import ply.yacc as yacc

from pyxie.model.pynode import *
from pyxie.parsing.lexer import tokens
from pyxie.parsing.context import *

class Grammar(object):
    precedence = (
        ('left', 'PLUS','MINUS'),
        ('left', 'TIMES','DIVIDE'),
        ('right', 'UMINUS')
    )
    tokens = tokens

    def p_error(self,p):
        print "Syntax error at", p

    def p_program(self, p):
        "program : statements"
        p[0] = PyProgram(p[1])

    def p_statements_1(self, p):
        "statements : statement"
        p[0] = PyStatements(p[1])

    def p_statements_2(self, p):
        "statements : statement statements"
        p[0] = PyStatements(p[1], p[2])

    def p_statement_1(self, p):
        "statement : assignment_statement"
        p[0] = p[1]

    def p_statement_2(self, p):
        "statement : print_statement"
        p[0] = p[1]

    def p_statement_3(self, p):
        "statement : general_expression"
        p[0] = PyExpressionStatement(p[1])

    def p_statement_4_empty(self, p):
        "statement : EOL"
        p[0] = PyEmptyStatement()

    def p_statement_5(self, p):
        "statement : while_statement"
        p[0] = p[1]

    def p_statement_6(self, p):
        "statement : break_statement"
        p[0] = p[1]

    def p_statement_7(self, p):
        "statement : continue_statement"
        p[0] = p[1]

    def p_statement_8(self, p):
        "statement : if_statement"
        p[0] = p[1]

    def p_statement_9(self, p):
        "statement : for_statement"
        p[0] = p[1]

    def p_break_statement_1(self, p):
        "break_statement : BREAK"
        p[0] = PyBreakStatement()

    def p_continue_statement_1(self, p):
        "continue_statement : CONTINUE"
        p[0] = PyContinueStatement()

    def p_print_statement_1(self, p):
        "print_statement : PRINT expr_list"
        p[0] = PyPrintStatement(p[2])


    def p_while_statement_1(self, p):
        "while_statement : WHILE general_expression COLON EOL statement_block"
        p[0] = PyWhileStatement(p[2], p[5]) # pass in expression and block
        print
        print "WARNING, expression used in a location requiring truthiness"                                     # TODO
        print "This will generally be OK for bools and integers but need a function for anything else"          # TODO
        print "In particular for strings, lists, dictionaries, tuples and so on"                                # TODO
        print "That is a separate card in the backlog though"                                                   # TODO
        print "SO WE REACHED WHILE"
        print "------------------> COND  :", p[2]
        print "------------------> BLOCK :", p[5]
        print "------------------> RESULT :", p[0]

    def p_if_statement_1(self, p):
        "if_statement : IF general_expression COLON EOL statement_block"
        print "PARSES IF"
        p[0] = PyIfStatement(p[2], p[5]) # pass in expression and block
        print
        print "WARNING, expression used in a location requiring truthiness"                                     # TODO
        print "This will generally be OK for bools and integers but need a function for anything else"          # TODO
        print "In particular for strings, lists, dictionaries, tuples and so on"                                # TODO
        print "That is a separate card in the backlog though"                                                   # TODO
        print "SO WE REACHED IF STATEMENT"
        print "------------------> COND  :", p[2]
        print "------------------> BLOCK :", p[5]
        print "------------------> RESULT :", p[0]

    def p_if_statement_2(self, p):
        "if_statement : IF general_expression COLON EOL statement_block extended_if_clauses"
        print "PARSES IF"
        p[0] = PyIfStatement(p[2], p[5],else_clause=p[6]) # pass in expression and block
        print
        print "WARNING, expression used in a location requiring truthiness"                                     # TODO
        print "This will generally be OK for bools and integers but need a function for anything else"          # TODO
        print "In particular for strings, lists, dictionaries, tuples and so on"                                # TODO
        print "That is a separate card in the backlog though"                                                   # TODO
        print "SO WE REACHED IF STATEMENT"
        print "------------------> COND  :", p[2]
        print "------------------> BLOCK :", p[5]
        print "------------------> RESULT :", p[0]

    def p_extended_if_clauses_1(self,p):
        "extended_if_clauses : else_clause"
        p[0] = p[1]

    def p_extended_if_clauses_2(self,p):
        "extended_if_clauses : elif_clause"
        p[0] = p[1]

    def p_else_clause_1(self,p):
        "else_clause : ELSE COLON EOL statement_block "
        p[0] = PyElseClause(p[4])


    def p_elif_clause_1(self, p):
        "elif_clause : ELIF general_expression COLON EOL statement_block"
        print "PARSES IF"
        p[0] = PyElIfClause(p[2], p[5]) # pass in expression and block
        print
        print "WARNING, expression used in a location requiring truthiness"                                     # TODO
        print "This will generally be OK for bools and integers but need a function for anything else"          # TODO
        print "In particular for strings, lists, dictionaries, tuples and so on"                                # TODO
        print "That is a separate card in the backlog though"                                                   # TODO
        print "SO WE REACHED IF STATEMENT"
        print "------------------> COND  :", p[2]
        print "------------------> BLOCK :", p[5]
        print "------------------> RESULT :", p[0]

    def p_elif_clause_2(self, p):
        "elif_clause : ELIF general_expression COLON EOL statement_block extended_if_clauses"
        print "PARSES IF"
        p[0] = PyElIfClause(p[2], p[5],else_clause=p[6]) # pass in expression and block
        print
        print "WARNING, expression used in a location requiring truthiness"                                     # TODO
        print "This will generally be OK for bools and integers but need a function for anything else"          # TODO
        print "In particular for strings, lists, dictionaries, tuples and so on"                                # TODO
        print "That is a separate card in the backlog though"                                                   # TODO
        print "SO WE REACHED IF STATEMENT"
        print "------------------> COND  :", p[2]
        print "------------------> BLOCK :", p[5]
        print "------------------> RESULT :", p[0]


    def p_for_statement_1(self, p):
        "for_statement : FOR IDENTIFIER IN general_expression COLON EOL statement_block"
        identifier = PyIdentifier(p.lineno(1), p[2])
        expression = p[4]
        statement_block = p[7]
        p[0] = PyForLoop(identifier, expression, statement_block)

    def p_block_1(self, p):
        "statement_block : INDENT statements DEDENT"
        p[0] = PyBlock(p[2])
        print
        print "SO WE REACHED BLOCK"
        print "------------------> STATEMENTS :", p[2]
        print "------------------> RESULT :", p[0]

    def p_expr_list_1(self,p):
        "expr_list : general_expression"
        p[0] = PyExprList(p[1])

    def p_expr_list_2(self,p):
        "expr_list : general_expression COMMA expr_list"
        p[0] = PyExprList(p[1],p[3])


    def p_assignment_statement(self, p):
        "assignment_statement : IDENTIFIER ASSIGN general_expression"
        identifier = PyIdentifier(p.lineno(1), p[1])

        p[0] = PyAssignment(identifier, p[3], p[2])

    def p_general_expression_1(self, p):
        "general_expression : boolean_expression"
        p[0] = p[1]

    def p_boolean_expression_1(self, p):
        "boolean_expression : boolean_and_expression"
        p[0] = p[1]

    def p_boolean_expression_2(self, p):
        "boolean_expression : boolean_expression OR boolean_and_expression"
        p[0] = PyOrOperator(p[1],p[3])

        print
        print "WARNING, expression used in a location requiring truthiness"                                     # TODO
        print "This will generally be OK for bools and integers but need a function for anything else"          # TODO
        print "In particular for strings, lists, dictionaries, tuples and so on"                                # TODO
        print "That is a separate card in the backlog though"                                                   # TODO
        print "SO WE REACHED AN OR EXPRESSION"
        print "------------------> LARG:", p[1]
        print "------------------> RARG :", p[3]
        print "------------------> RESULT :", p[0]

    def p_boolean_and_expression_1(self, p):
        "boolean_and_expression : boolean_not_expression"
        p[0] = p[1]

    def p_boolean_and_expression_2(self, p):
        "boolean_and_expression  : boolean_and_expression AND boolean_not_expression"
        p[0] = PyAndOperator(p[1],p[3])
        print
        print "WARNING, expression used in a location requiring truthiness"                                     # TODO
        print "This will generally be OK for bools and integers but need a function for anything else"          # TODO
        print "In particular for strings, lists, dictionaries, tuples and so on"                                # TODO
        print "That is a separate card in the backlog though"                                                   # TODO
        print "SO WE REACHED AN AND EXPRESSION"
        print "------------------> LARG:", p[1]
        print "------------------> RARG :", p[3]
        print "------------------> RESULT :", p[0]

    def p_boolean_not_expression_1(self, p):
        "boolean_not_expression : relational_expression"
        p[0] = p[1]

    def p_boolean_not_expression_2(self, p):
        "boolean_not_expression : NOT boolean_not_expression "
        p[0] = PyNotOperator(p[2])
        print
        print "WARNING, expression used in a location requiring truthiness"                                     # TODO
        print "This will generally be OK for bools and integers but need a function for anything else"          # TODO
        print "In particular for strings, lists, dictionaries, tuples and so on"                                # TODO
        print "That is a separate card in the backlog though"                                                   # TODO
        print "SO WE REACHED AN AND EXPRESSION"
        print "------------------> ARG:", p[2]
        print "------------------> RESULT :", p[0]

    def p_relational_expression_1(self, p):
        "relational_expression : relational_expression COMPARISON_OPERATOR expression"
        p[0] = PyComparisonOperator(p[2], p[1], p[3])

    def p_relational_expression_2(self, p):
        "relational_expression : expression"
        p[0] = p[1]

    def p_expression_1(self, p):
        "expression : arith_expression"
        p[0] = p[1]

    def p_expression_2(self, p):
        "expression : expression PLUS arith_expression"
        p[0] = PyPlusOperator(p[1],p[3])

    def p_expression_3(self, p):
        "expression : expression MINUS arith_expression"
        p[0] = PyMinusOperator(p[1],p[3])

    def p_expression_4(self, p):
        "expression : expression POWER arith_expression"
        p[0] = PyPowerOperator(p[1],p[3])

    def p_arith_expression_1(self, p):
        "arith_expression     : expression_atom"
        p[0] = p[1]

    def p_arith_expression_2(self, p):
        "arith_expression     : arith_expression TIMES expression_atom"
        p[0] = PyTimesOperator(p[1],p[3])

    def p_arith_expression_3(self, p):
        "arith_expression     : arith_expression DIVIDE expression_atom"
        p[0] = PyDivideOperator(p[1],p[3])

    def p_expression_atom_1(self, p):
        "expression_atom : value_literal"
        p[0] = p[1]

    def p_expression_atom_2(self, p):
        "expression_atom : IDENTIFIER PARENL expr_list PARENR"
        p[0] = PyFunctionCall(PyIdentifier(p.lineno(1), p[1]), p[3])

    def p_expression_atom_3(self, p):
        "expression_atom : PARENL general_expression PARENR"
        p[0] = p[2]

    ### Core Literals

    def p_value_literal_0(self, p):
        "value_literal : number"
        p[0] = p[1]

    def p_value_literal_1(self, p):
        "number : NUMBER"
        p[0] = PyInteger(p.lineno(1), p[1])

    def p_value_literal_2(self, p):
        "number : FLOAT"
        p[0] = PyFloat(p.lineno(1), p[1])

    def p_value_literal_3(self, p):
        "number : HEX"
        p[0] = PyHex(p.lineno(1), p[1])

    def p_value_literal_4(self, p):
        "number : OCTAL"
        p[0] = PyOctal(p.lineno(1), p[1])

    def p_value_literal_5(self, p):
        "number : BINARY"
        p[0] = PyBinary(p.lineno(1), p[1])

    def p_value_literal_5a(self,p):
        "number : MINUS number %prec UMINUS"
        p[0] = p[2].negate()

    def p_value_literal_6(self, p):
        "value_literal : STRING"
        p[0] = PyString(p.lineno(1), p[1])

    def p_value_literal_6a(self, p):
        "value_literal : CHARACTER"
        p[0] = PyCharacter(p.lineno(1), p[1])

    def p_value_literal_7(self, p):
        "value_literal : BOOLEAN"
        p[0] = PyBoolean(p.lineno(1), p[1])

    def p_value_literal_8(self, p):
        "value_literal : IDENTIFIER"
        p[0] = PyIdentifier(p.lineno(1), p[1])

def parse(source,lexer):

   if not source.endswith("\n"): # Be relaxed about end of file
       source = source+ "\n"

   yacc.yacc(module=Grammar())
   result = yacc.parse(source, lexer=lexer)
   return result
