#-------------------------------------------------------------------------------
# refactor.py
#
#
# Copyright (C) 2015, Ryosuke Fukatani
# License: Apache 2.0
#-------------------------------------------------------------------------------

import sys
import os
import copy
import collections

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )

import pyverilog.utils.version
from pyverilog.vparser.ply.yacc import *
from pyverilog.utils.util import *
from pyverilog.dataflow.dataflow import *
from pyverilog_toolbox.verify_tool.dataflow_facade import *
from pyverilog_toolbox.verify_tool.bindlibrary import *

import pyverilog.controlflow.splitter as splitter


class Refactor(dataflow_facade):

    def search_unreferenced(self):
        """[FUNCTIONS]
        search input/reg/wire which not referenced any other output/reg/wire.
        """
        signals = []
        for tv,tk in self.binds.walk_signal():
            if not set(['Input', 'Reg', 'Wire']) & tv.termtype: continue
            if 'Output' in tv.termtype: continue
            signals.append(str(tk))

        for tv,tk,bvi,bit,term_lsb in self.binds.walk_reg_each_bit():
            target_tree = self.makeTree(tk)
            trees = self.binds.extract_all_dfxxx(target_tree, set([]), bit, pyverilog.dataflow.dataflow.DFTerminal)
            trees.add((bvi.getClockName(), bvi.getClockBit()))
            trees.add((bvi.getResetName(), bvi.getResetBit()))
            for tree, bit in trees:
                if str(tree) in signals:
                    signals.remove(str(tree))
        print signals
        return signals

def parse_for_refactor(self, text, debug=0):
    """ [FUNCTIONS]
    for override pyverilog.vparser.parser.VerilogParser.parse
    """
    return self.parser.parse(text, lexer=self.lexer.lexer, tracking=True, debug=debug)

#TODO
def parse_vcp_for_refactor(self, preprocess_output='preprocess.output', debug=0):
    """ [FUNCTIONS]
    for override pyverilog.vparser.parser.VerilogCodeParser.parse
    """
    text = self.preprocess()
    ast = self.parser.parse(text, debug=debug).value
    self.directives = self.parser.get_directives()
    return ast

#TODO
def parse_lrp(self,input=None,lexer=None,debug=0,tracking=0,tokenfunc=None):
    if debug or yaccdevel:
        if isinstance(debug,int):
            debug = PlyLogger(sys.stderr)
        return self.parsedebug(input,lexer,debug,tracking,tokenfunc)
    elif tracking:
        return self.parseopt(input,lexer,debug,tracking,tokenfunc)
    else:
        return self.parseopt_notrack(input,lexer,debug,tracking,tokenfunc)

#TODO
def parseopt_for_refactor(self,input=None,lexer=None,debug=0,tracking=0,tokenfunc=None):
    """ [FUNCTIONS]
    for override pyverilog.vparser.ply.yacc.LRParser.parseopt
    """
    lookahead = None                 # Current lookahead symbol
    lookaheadstack = [ ]             # Stack of lookahead symbols
    actions = self.action            # Local reference to action table (to avoid lookup on self.)
    goto    = self.goto              # Local reference to goto table (to avoid lookup on self.)
    prod    = self.productions       # Local reference to production list (to avoid lookup on self.)
    pslice  = YaccProduction(None)   # Production object passed to grammar rules
    errorcount = 0                   # Used during error recovery

    # If no lexer was given, we will try to use the lex module
    if not lexer:
        lex = load_ply_lex()
        lexer = lex.lexer

    # Set up the lexer and parser objects on pslice
    pslice.lexer = lexer
    pslice.parser = self

    # If input was supplied, pass to lexer
    if input is not None:
        lexer.input(input)

    if tokenfunc is None:
       # Tokenize function
       get_token = lexer.token
    else:
       get_token = tokenfunc

    # Set up the state and symbol stacks

    statestack = [ ]                # Stack of parsing states
    self.statestack = statestack
    symstack   = [ ]                # Stack of grammar symbols
    self.symstack = symstack

    pslice.stack = symstack         # Put in the production
    errtoken   = None               # Err token

    # The start state is assumed to be (0,$end)

    statestack.append(0)
    sym = YaccSymbol()
    sym.type = '$end'
    symstack.append(sym)
    state = 0
    while 1:
        # Get the next symbol on the input.  If a lookahead symbol
        # is already set, we just use that. Otherwise, we'll pull
        # the next token off of the lookaheadstack or from the lexer

        if not lookahead:
            if not lookaheadstack:
                lookahead = get_token()     # Get the next token
            else:
                lookahead = lookaheadstack.pop()
            if not lookahead:
                lookahead = YaccSymbol()
                lookahead.type = '$end'

        # Check the action table
        ltype = lookahead.type
        t = actions[state].get(ltype)

        if t is not None:
            if t > 0:
                # shift a symbol on the stack
                statestack.append(t)
                state = t

                symstack.append(lookahead)
                lookahead = None

                # Decrease error count on successful shift
                if errorcount: errorcount -=1
                continue

            if t < 0:
                # reduce a symbol on the stack, emit a production
                p = prod[-t]
                pname = p.name
                plen  = p.len

                # Get production function
                sym = YaccSymbol()
                sym.type = pname       # Production name
                sym.value = None

                if plen:
                    targ = symstack[-plen-1:]
                    targ[0] = sym

                    # --! TRACKING
                    if tracking:
                       t1 = targ[1]
                       sym.lineno = t1.lineno
                       sym.lexpos = t1.lexpos
                       t1 = targ[-1]
                       sym.endlineno = getattr(t1,"endlineno",t1.lineno)
                       sym.endlexpos = getattr(t1,"endlexpos",t1.lexpos)

                    # --! TRACKING

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # The code enclosed in this section is duplicated
                    # below as a performance optimization.  Make sure
                    # changes get made in both locations.

                    pslice.slice = targ

                    try:
                        # Call the grammar rule with our special slice object
                        del symstack[-plen:]
                        del statestack[-plen:]
                        p.callable(pslice)
                        symstack.append(sym)
                        state = goto[statestack[-1]][pname]
                        statestack.append(state)
                    except SyntaxError:
                        # If an error was set. Enter error recovery state
                        lookaheadstack.append(lookahead)
                        symstack.pop()
                        statestack.pop()
                        state = statestack[-1]
                        sym.type = 'error'
                        lookahead = sym
                        errorcount = error_count
                        self.errorok = 0
                    continue
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                else:

                    # --! TRACKING
                    if tracking:
                       sym.lineno = lexer.lineno
                       sym.lexpos = lexer.lexpos
                    # --! TRACKING

                    targ = [ sym ]

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # The code enclosed in this section is duplicated
                    # above as a performance optimization.  Make sure
                    # changes get made in both locations.

                    pslice.slice = targ

                    try:
                        # Call the grammar rule with our special slice object
                        p.callable(pslice)
                        symstack.append(sym)
                        state = goto[statestack[-1]][pname]
                        statestack.append(state)
                    except SyntaxError:
                        # If an error was set. Enter error recovery state
                        lookaheadstack.append(lookahead)
                        symstack.pop()
                        statestack.pop()
                        state = statestack[-1]
                        sym.type = 'error'
                        lookahead = sym
                        errorcount = error_count
                        self.errorok = 0
                    continue
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if t == 0:
                n = symstack[-1]
                #return getattr(n,"value",None)
                return n

        if t == None:

            # We have some kind of parsing error here.  To handle
            # this, we are going to push the current token onto
            # the tokenstack and replace it with an 'error' token.
            # If there are any synchronization rules, they may
            # catch it.
            #
            # In addition to pushing the error token, we call call
            # the user defined p_error() function if this is the
            # first syntax error.  This function is only called if
            # errorcount == 0.
            if errorcount == 0 or self.errorok:
                errorcount = error_count
                self.errorok = 0
                errtoken = lookahead
                if errtoken.type == '$end':
                    errtoken = None               # End of file!
                if self.errorfunc:
                    global errok,token,restart
                    errok = self.errok        # Set some special functions available in error recovery
                    token = get_token
                    restart = self.restart
                    if errtoken and not hasattr(errtoken,'lexer'):
                        errtoken.lexer = lexer
                    tok = self.errorfunc(errtoken)
                    del errok, token, restart   # Delete special functions

                    if self.errorok:
                        # User must have done some kind of panic
                        # mode recovery on their own.  The
                        # returned token is the next lookahead
                        lookahead = tok
                        errtoken = None
                        continue
                else:
                    if errtoken:
                        if hasattr(errtoken,"lineno"): lineno = lookahead.lineno
                        else: lineno = 0
                        if lineno:
                            sys.stderr.write("yacc: Syntax error at line %d, token=%s\n" % (lineno, errtoken.type))
                        else:
                            sys.stderr.write("yacc: Syntax error, token=%s" % errtoken.type)
                    else:
                        sys.stderr.write("yacc: Parse error in input. EOF\n")
                        return

            else:
                errorcount = error_count

            # case 1:  the statestack only has 1 entry on it.  If we're in this state, the
            # entire parse has been rolled back and we're completely hosed.   The token is
            # discarded and we just keep going.

            if len(statestack) <= 1 and lookahead.type != '$end':
                lookahead = None
                errtoken = None
                state = 0
                # Nuke the pushback stack
                del lookaheadstack[:]
                continue

            # case 2: the statestack has a couple of entries on it, but we're
            # at the end of the file. nuke the top entry and generate an error token

            # Start nuking entries on the stack
            if lookahead.type == '$end':
                # Whoa. We're really hosed here. Bail out
                return

            if lookahead.type != 'error':
                sym = symstack[-1]
                if sym.type == 'error':
                    # Hmmm. Error is on top of stack, we'll just nuke input
                    # symbol and continue
                    lookahead = None
                    continue
                t = YaccSymbol()
                t.type = 'error'
                if hasattr(lookahead,"lineno"):
                    t.lineno = lookahead.lineno
                t.value = lookahead
                lookaheadstack.append(lookahead)
                lookahead = t
            else:
                symstack.pop()
                statestack.pop()
                state = statestack[-1]       # Potential bug fix

            continue

        # Call an error function here
        raise RuntimeError("yacc: internal parser error!!!\n")

if __name__ == '__main__':
    pyverilog.vparser.parser.VerilogParser.parse = MethodType(parse_for_refactor, None, pyverilog.vparser.parser.VerilogParser)
    pyverilog.vparser.parser.VerilogCodeParser.parse = MethodType(parse_vcp_for_refactor, None, pyverilog.vparser.parser.VerilogCodeParser)
    pyverilog.vparser.ply.yacc.LRParser.parseopt = MethodType(parseopt_for_refactor, None, pyverilog.vparser.ply.yacc.LRParser)
    pyverilog.vparser.ply.yacc.LRParser.parse = MethodType(parse_lrp, None, pyverilog.vparser.ply.yacc.LRParser)
    u_finder = Refactor("../testcode/simple.v")
    u_finder.search_unreferenced()



