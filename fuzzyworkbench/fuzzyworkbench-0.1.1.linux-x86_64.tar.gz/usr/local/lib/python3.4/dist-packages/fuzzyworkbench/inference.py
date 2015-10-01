from tkinter import *
from tkinter.ttk import *
from fuzzylib.fis import FIS

#@TODO Update results whenever inputs changes

class Inference(Frame):
    def __init__(self, master, app, **kw):
        Frame.__init__(self, master, **kw)
        self._app = app
        self._inputs = Frame(self)    
        self._inputs.pack(side=LEFT, expand=1, fill=Y, padx=10)
        self._outputs = Frame(self)
        self._outputs.pack(side=LEFT, expand=1, fill=Y, padx=10)
        self._varInputs = {}
        self._varOutputs = {}
        self._varRanges = {} #dict of tuples
        
    def updateWidgets(self):
        #Clearing previous data and widgets
        for widget in self._inputs.winfo_children():
            widget.destroy()
        for widget in self._outputs.winfo_children():
            widget.destroy()
        for i in self._varInputs:
            for t in self._varInputs[i].trace_vinfo():
                self._varInputs[i].trace_vdelete(*t)
        self._varInputs.clear()
        self._varOutputs.clear()
        self._varRanges.clear()
        #Getting variables ranges
        self._variables = self._app.getVars()
        for v in self._variables:
            self._varRanges[v.get_name()] = v.get_range()
        #Getting variables list based on rules
        self._rules = self._app.getRules()
        invars = set()
        outvars = set()
        for r in self._rules:
            outvars.add(r.get_consequent()[0])
            for element in r.get_antecedent():
                if type(element) == tuple:
                    invars.add(element[0])
        invars = list(invars)
        outvars = list(outvars)
        invars.sort()        
        outvars.sort()
        #Creating input widgets
        row = 0
        for i in invars:
            Label(self._inputs, text=i + '=').grid(row=row, column=0)
            self._varInputs[i] = StringVar()
            minval, maxval = self._varRanges[i]
            self._varInputs[i].set( (maxval + minval) / 2)
            spin = Spinbox(self._inputs, from_=minval, to=maxval)
            spin['textvariable'] = self._varInputs[i]
            spin.grid(row=row, column=1, sticky='we')
            self._varInputs[i].trace('w', self.compute)
            row += 1
        #Creating output widgets
        row = 0
        for o in outvars:
            Label(self._outputs, text=o + '=').grid(row=row, column=0)
            self._varOutputs[o] = StringVar()
            label = Label(self._outputs, text='')
            label['textvariable'] = self._varOutputs[o]
            label.grid(row=row, column=1, sticky='we')
            row += 1
        self.compute()
        
    def compute(self, *args):
        fis = FIS()
        for v in self._variables:
            fis.add_variable(v)
        for r in self._rules:
            fis.add_rule(r)
        
        inputValues = {}
        for key, value in self._varInputs.items():
            try:
                val = float(value.get())
                inputValues[key] = val
            except ValueError:
                for i in self._varOutputs:
                    self._varOutputs[i].set('')
                return
                       
        outputs = fis.defuzzy(inputValues)
        for i in outputs:
            self._varOutputs[i].set(outputs[i])
