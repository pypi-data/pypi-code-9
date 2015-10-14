__author__ = 'larsvoegtlin'

from pyparsing import *

from _dsl.helpers import convertToFloat


#Grundvariablen
numbers = Word( nums )
numbersNegative = Combine(Literal("-") + numbers)
integer = Or([numbers, numbersNegative]).setParseAction(convertToFloat)

alphabet = "abcdefghijklmnopqrstuvwxyz"
word = Word(alphabet)

operator = Or([Literal("<"), Literal(">"), Literal("="), Literal(">="), Literal("<="), Literal("!=")])

true = Keyword("true").setParseAction( replaceWith(True))
false = Keyword("false").setParseAction( replaceWith(False))
boolean = Or([true, false])

value = Or([integer, boolean, word]) #akzeptiert string, integer und boolean

#v3 der Grammatik akzeptiert (abc#def!=-20(ghi#jkl=true)) -> [['abc', 'def', '!=', -20, ['ghi', 'jkl', '=', True]]]
path = word + Optional(Suppress("#") + word)

command = path("path") + operator("operator") + value("value")

grammar = Forward()
parens = nestedExpr('(', ')', content=command)
grammar <<= OneOrMore((parens)("test"))

try:
    print grammar.parseString("(abc#def!=-20(ghi#jkl=true))")
except ParseException:
    print "Error while parsing"