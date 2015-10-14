__author__ = 'larsvoegtlin'

from pyparsing import *

#Grundvariablen
numbers = Word( nums )
numbersNegative = Group("-" + numbers)
integer = Or([numbers, numbersNegative])

alphabet = "abcdefghijklmnopqrstuvwxyz"
word = Word(alphabet)

operator = Word("><=", max=1) #Damit nicht meh als ein oparator eingegeben werden kann

true = Keyword("true").setParseAction( replaceWith(True))
false = Keyword("false").setParseAction( replaceWith(False))
boolean = Or([true, false])

value = Or([integer, boolean]) #akzeptiert nur integer und boolean

#v1 der Grammatik akzeptiert abc#def<-30 -> ['abc', '#', 'def', '<', ['-', '30']]
path = word + "#" + word

command = path + operator + value

try:
    print command.parseString("abc#def<30")
except ParseException:
    print "Error while parsing"
