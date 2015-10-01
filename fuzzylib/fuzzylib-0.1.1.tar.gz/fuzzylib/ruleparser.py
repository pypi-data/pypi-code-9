from collections import OrderedDict
from pyparsing import (CaselessLiteral, Literal, Word, ZeroOrMore, Forward, 
                       nums, alphas, oneOf)
from fuzzylib.rule import Rule

class RuleParser(object):

    def __init__(self):
        """
        Grammar (Adapted from fourFn.py example)
        atom    :: identifier IS identifier | '(' expr ')'
        term    :: atom [ AND atom ]*
        expr    :: term [ OR term ]*
        rule    :: IF expr THEN identifier IS identifier
        """
        
        self._vars = OrderedDict()      #linguistic variables
        
        #Tokens (identifiers, operators and parenthesis)
        lit_and = CaselessLiteral("AND")
        lit_or = CaselessLiteral("OR")
        lit_is = CaselessLiteral("IS")
        lit_if = CaselessLiteral("IF")
        lit_then = CaselessLiteral("THEN")
        ident = Word(alphas, alphas + nums)
        lpar  = Literal( "(" ).suppress()
        rpar  = Literal( ")" ).suppress()
        
        #Gramática
        expr = Forward()
        atom = ( 
            (ident + lit_is + ident).setParseAction(self._compile_proposition) | 
            (lpar + expr + rpar) 
        )
        term = atom + ZeroOrMore( 
            ( lit_and + atom ).setParseAction( self._push_first ) 
        )
        expr << term + ZeroOrMore( 
            ( lit_or + term ).setParseAction( self._push_first ) )
        rule = lit_if + expr + lit_then + \
              (ident + lit_is + ident).setParseAction(self._compile_consequent)
        self.bnf = rule
        
    def add_variable(self, var):
        self._vars[var.get_name()] = var
        
    def _compile_proposition(self, string, loc, toks):
        op1, lit_is, op2 = toks
        function = self._vars[op1].get_set(op2)
        self._stack.append( (op1, function) )
        
    def _compile_consequent(self, string, loc, toks):
        op1, lit_is, op2 = toks
        function = self._vars[op1].get_set(op2)
        self._consequent = (op1, function)
        
    def _push_first(self, strg, loc, toks):
        if toks[0] == 'AND':
            self._stack.append(min)
        elif toks[0] == 'OR':
            self._stack.append(max)
        else:
            self._stack.append(toks[0])

    def compile_rule(self, rule, parseAll=True):
        self._stack = []
        self._consequent = ()
        results = self.bnf.parseString(rule, parseAll)
        return Rule(self._stack, self._consequent)
