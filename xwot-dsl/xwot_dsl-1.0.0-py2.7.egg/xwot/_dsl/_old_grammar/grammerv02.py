__author__ = 'larsvoegtlin'

from pyparsing import *

from _dsl.helpers import convertToFloat


#Grundvariablen
numbers = Word( nums )
numbersNegative = Combine(Literal("-") + numbers)
integer = Or([numbers, numbersNegative]).setParseAction(convertToFloat)

alphabet = "abcdefghijklmnopqrstuvwxyz"
word = Word(alphabet)

operator = Or([Literal("<"), Literal(">"), Literal("=")])

true = Keyword("true").setParseAction( replaceWith(True))
false = Keyword("false").setParseAction( replaceWith(False))
boolean = Or([true, false])

value = Or([integer, boolean, word]) #akzeptiert string, integer und boolean

#v2 der Grammatik akzeptiert abc#def=-20 -> {'operator': '=', 'path': (['abc', 'def'], {}), 'value': -20}
path = word + Optional(Suppress("#") + word)

command = path.setResultsName("path") + operator.setResultsName("operator") + value.setResultsName("value")

try:
    test = command.parseString("abc#def=hallo")
    dic = test.asDict()
    print dic
    print dic['path']
except ParseException:
    print "Error while parsing"