__author__ = 'larsvoegtlin'

from pyparsing import *

from helpers import convertToFloat, dictToString
import messages as EXCEPTION


class grammar():
    def __init__(self, sensors):
        self.__sensors = dictToString(sensors)

    def __creategrammar(self):
        # Grundvariablen
        numbers = Word(nums).setName(EXCEPTION.EXCEPTION_VALUE)
        numbersNegative = Combine(Literal("-") - numbers).setName(EXCEPTION.EXCEPTION_VALUE)
        integer = Or([numbers, numbersNegative]).setParseAction(convertToFloat)

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        word = Word(alphabet)

        operatorsRaw = [Literal("<"), Literal(">"), Literal("=").setParseAction(replaceWith("==")), Literal("=="),
                        Literal(">="), Literal("<="), Literal("!=")]
        for op in operatorsRaw:
            op.setName(EXCEPTION.EXCEPTION_OPERATOR)

        operatorGrammar = Or(operatorsRaw)

        true = Keyword("true").setParseAction(replaceWith(True)).setName(EXCEPTION.EXCEPTION_VALUE)
        false = Keyword("false").setParseAction(replaceWith(False)).setName(EXCEPTION.EXCEPTION_VALUE)
        boolean = Or([true, false])

        # akzeptiert string, integer und boolean
        value = Or([integer, boolean, word])

        logicalOperation = Or([Literal("&").setName(EXCEPTION.EXCEPTION_PARENSLOOP),
                               Literal("|").setName(EXCEPTION.EXCEPTION_PARENSLOOP)])
        openParens = Suppress(Literal("(").setName(EXCEPTION.EXCEPTION_PARENSLOOP))
        closeParens = Suppress(Literal(")").setName(EXCEPTION.EXCEPTION_PARENSLOOP))

        # v5 der Grammatik akzeptiert (abc#def!=-20)&((ghi#jkl=true)|(mno#pqr>=25))) ->
        # [['abc#def', '>=', 20], '&', [['ghi#jkl', '==', True], '|', ['mno#pqr#stu', '>=', 25]]]
        path = oneOf(self.__sensors).setName(EXCEPTION.EXCEPTION_PATH)

        command = Forward()
        commandTuple = Group(path - operatorGrammar - value | command)
        command << openParens - commandTuple - closeParens - Optional(logicalOperation) - Optional(command)

        grammar = OneOrMore(command)
        return grammar

    def parse(self, stringtoparse):
        try:
            return self.__creategrammar().parseString(stringtoparse, parseAll=True).asList()
        except (ParseException, ParseSyntaxException) as e:
            return "Error while parsing", e
