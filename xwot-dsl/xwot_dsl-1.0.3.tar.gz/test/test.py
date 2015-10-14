__author__ = 'larsvoegtlin'

from xwot_dsl.helpers import *
from xwot_dsl.xwot_dsl import *

# legende: g -> grammatik, h -> helpers, s -> solver, a -> ein gesammter durchlauf durchs system
# all -> alle test werden ausgefuehrt, d = xwot_dsl modul
tests = ['all']

jsonDict = {"temperature": {"@units": "celsisus", "@precision": "2", "#text": "24.30"},
            "humidity": {"@units": "celsisus", "@precision": "2", "#text": "46.60"},
            "electricity": "1", "timestamp": "1441273403"}
commandList = [['temperature,#text', '==', 20], '&', [['temperature,#text', '==', True], '&',
                                                     ['temperature,#text', '==', 'hello']]]

def helperTests():
    print "------------"
    print "helper test"
    print "------------"
    print splitUpPath("abc,@def")  # custom exceptions gehen nicht, sollte jedoch kein problem sein
    print dictToString(jsonDict)
    print getValueFromJson(jsonDict, ['temperature', '#text'])
    l = ['temperature,#text', '>=', 20.00]
    l[0] = getValueFromJson(jsonDict, splitUpPath(l[0]))
    print l
    replacePath(jsonDict, commandList)
    print commandList
    print listToAstString(commandList)
    print "**********"


def grammerTests():
    print "------------"
    print "grammar test"
    print "------------"
    g = grammar({'abc': '#def', 'ghi': '#jkl', 'mno': {'#pqr': '#stu'}})
    print g.parse("(abc>=20)&((ghi=true)|(mno,#pqr>=25))")  # ok
    print g.parse("(ab>=20)&((ghi=true)|(mno,#pqr>=25))")  # path error
    print g.parse("(abc20)&((ghi=true)|(mno,#pqr>=25))")  # operator error
    print g.parse("(abc>=@)&((ghi=true)|(mno,#pqr>=25))")  # value error
    print g.parse("(abc>=20)&((hi=true)|(mno,#pqr>=25))")  # Fehler wird geworfen -> g fehlt
    print g.parse("(abc>=20)&((ghi=true)R(mno,#pqr>=25))")  # falscher operator, fehler wird nicht geworfen
    print g.parse("(abc>=20)&((ghi=true)|(mno,#pqr>=25)")  # falsche klammern, Fehler wird nicht immer geworfen
    print "**********"


def solverTests():
    print "------------"
    print "solver test"
    print "------------"
    print astSolver("((24.30 >= 20.0) & ((46.60 == True) | (1 == 'celsisus')))")
    print astSolver("((24.30 >= 20.0) & ((True == True) | (1 == 'celsisus')))")
    print "**********"


def allTest():
    print "------------"
    print "full test"
    print "------------"
    # sollte true returnen
    inputString = "(temperature,#text>=20)&((humidity,#text=true)|(humidity,@units=celsisus))"
    gram = grammar(jsonDict)
    inputList = gram.parse(inputString)
    replacePath(jsonDict, inputList)
    tree = listToAstString(inputList)
    print astSolver(tree)
    # sollte false returnen
    inputString = "(temperature,#text>=30)&((humidity,#text=true)|(humidity,@units=celsisus))"
    gram = grammar(jsonDict)
    inputList = gram.parse(inputString)
    replacePath(jsonDict, inputList)
    tree = listToAstString(inputList)
    print astSolver(tree)
    print "**********"

def dslTests():
    print "------------"
    print "dslmodule test"
    print "------------"
    dsl = dslmodule(jsonDict)
    validate = dsl.validate("(temperature,#text>=20)&((humidity,#text=true)|(humidity,@units=celsisus))")
    print validate
    evalute = dsl.evaluate(validate)
    print evalute
    print "**********"

for t in tests:
    if t == 'h':
        helperTests()
    elif t == 'g':
        grammerTests()
    elif t == 's':
        solverTests()
    elif t == 'a':
        allTest()
    elif t == 'd':
        dslTests()
    elif t == 'all':
        helperTests()
        grammerTests()
        solverTests()
        allTest()
        dslTests()
