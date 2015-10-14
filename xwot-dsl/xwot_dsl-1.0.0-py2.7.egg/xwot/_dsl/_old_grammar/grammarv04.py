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

true = Keyword("true").setParseAction(replaceWith(True))
false = Keyword("false").setParseAction(replaceWith(False))
boolean = Or([true, false])

value = Or([integer, boolean, word]) #akzeptiert string, integer und boolean

logicalOperation = Or([Literal("&"), Literal("|")])
openParens = Suppress(Literal("("))
closeParens = Suppress(Literal(")"))

#v4 der Grammatik akzeptiert (abc#def!=-20)&((ghi#jkl=true)|(mno#pqr>=25))) -> [['abc', 'def', '!=', -20], '&', [['ghi', 'jkl', '=', True], '|', ['mno', 'pqr', '>=', 25]]]
path = word + Optional(Suppress("#") + word)

command = Forward()
command << openParens + Group(path + operator + value | command) + closeParens + Optional(logicalOperation) + Optional(command)

grammar = OneOrMore(command)

try:
    print grammar.parseString("(abc#def!=-20)&((ghi#jkl=true)|(mno#pqr>=25))").asList()
except ParseException:
    print "Error while parsing"