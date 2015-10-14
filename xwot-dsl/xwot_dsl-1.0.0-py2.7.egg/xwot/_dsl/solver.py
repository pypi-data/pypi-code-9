import ast

__author__ = 'larsvoegtlin'

# s = der Tree als string, welcher ausgewertet werden soll
def astSolver(s):
    tree = ast.parse(s, mode="eval")
    return eval(compile(tree, '<string>', mode='eval'))

