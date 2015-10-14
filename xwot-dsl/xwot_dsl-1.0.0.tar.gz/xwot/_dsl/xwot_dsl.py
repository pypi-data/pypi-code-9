__author__ = 'larsvoegtlin'
from _dsl.grammarv05 import grammar
from _dsl.helpers import replacePath, listToAstString
from _dsl.solver import astSolver

class dslmodule:
    def __init__(self, sensors):
        self.__sensors = sensors

    def validate(self, inputString):
        valiList = grammar(self.__sensors).parse(inputString)
        #valilist muss noch gespeichert werden.
        return valiList

    def evaluate(self, grammerList):
        replacePath(self.__sensors, grammerList)
        tree = listToAstString(grammerList)
        return astSolver(tree)
