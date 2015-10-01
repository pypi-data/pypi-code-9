import math

class FIS:
    def __init__(self):
        self._rules = {} # rule list (dict value) for each output var (dict key)
        self._variables = {} # LinguisticVars, indexed by name
        
    def add_rule(self, rule):
        #Config: add compiled rules to inference system
        outvar = rule.get_consequent()[0]
        if outvar not in self._rules:
            self._rules[outvar] = []
        self._rules[outvar].append(rule)
        
    def add_variable(self, var):
        #Config: add linguistic variables to inference system
        self._variables[var.get_name()] = var
        
    def _process_output(self, rules, vars_values):
        outvar = self._variables[ rules[0].get_consequent()[0] ]
        center_num = 0
        center_den = 0
        xmin, xmax = outvar.get_range()
        x = xmin
        xstep = (xmax - xmin) / 1000
        while x < xmax:
            #Rules Activation
            activation = []
            for r in rules:
                for var in vars_values:
                    r.set_value(var, vars_values[var])
                ant = r.eval_antecedent()
                function = r.get_consequent()[1]
                activation.append(min(ant, function(x)))
            #Aggregation
            fx = max(activation)
            #Center of Area
            center_num += x * fx
            center_den += fx
            #Next x
            x += xstep
        try:
            value = center_num / center_den
        except ZeroDivisionError:
            value = float('inf')
        return value
        
    def defuzzy(self, vars_values):
        #Per-output defuzzyfication
        outputs = {}
        for o in self._rules:
            outputs[o] = self._process_output(self._rules[o], vars_values)
        return outputs
