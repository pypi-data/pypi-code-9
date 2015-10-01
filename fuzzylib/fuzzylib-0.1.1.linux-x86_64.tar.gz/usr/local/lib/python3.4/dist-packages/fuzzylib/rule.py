from collections import OrderedDict

class Rule:
    def __init__(self, antecedent, consequent):
        self._antecedent = antecedent #compiled antecedent as an array
        self._consequent = consequent #compiled consequent as tuple
        self._varValues = OrderedDict()
        
    def set_value(self, varname, value):
        self._varValues[varname] = value
        
    def get_antecedent(self):
        return self._antecedent
        
    def get_consequent(self):
        return self._consequent
        
    def eval_antecedent(self):
        eval_stack = []
        for x in self._antecedent:
            if type(x) == tuple: #proposição
                value = self._varValues[x[0]]
                function = x[1]
                eval_stack.append(function(value))
            elif callable(x):
                op1 = eval_stack.pop()
                op2 = eval_stack.pop()
                eval_stack.append(x(op1, op2))
        return eval_stack[0]
        
