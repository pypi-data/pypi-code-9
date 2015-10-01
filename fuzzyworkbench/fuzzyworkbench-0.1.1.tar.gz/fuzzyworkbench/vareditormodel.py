from tkinter import *
from tkinter.ttk import *
from fuzzyworkbench.managedmodel import ManagedModel
from fuzzyworkbench.common import functionTypes, paramCount

class VarEditorModel(ManagedModel):
    def __init__(self, editor, name, minval, maxval):
        ManagedModel.__init__(self, editor)
        self.name = StringVar(value=name)
        self.name.trace('w', self._do_changed)
        self.minval = StringVar(value=minval)
        self.minval.trace('w', self._do_changed)
        self.maxval = StringVar(value=maxval)
        self.maxval.trace('w', self._do_changed)
        self._functions = []
    def getFunctions(self):
        return self._functions
    def addFunction(self, function):
        self._functions.append(function)
        self._do_changed()
    def removeFunction(self, function):
        self._functions.remove(function)
        self._do_changed()
    def __str__(self):
        return self.name.get()
        
class VarEditorFunction(ManagedModel):
    def __init__(self, editor, name, fntype):
        ManagedModel.__init__(self, editor)
        self.name = StringVar(value=name)
        self.name.trace('w', self._do_changed)
        self.fntype = StringVar(value=fntype) #initial fntype
        self.fntype.trace('w', self._do_changed)
        self.params = {}     #parameter list for all fntypes available
        for i in functionTypes:
            self.params[i] = []
            for x in range(paramCount[i]):
                self.params[i].append(StringVar())
    def setParams(self, fntype, params):
        self.params[fntype] = []
        for i in params:
            var = StringVar(value=i)
            self.params[fntype].append(var)
        self._do_changed()
    def getCurrParams(self):
        return self.params[self.fntype.get()]
