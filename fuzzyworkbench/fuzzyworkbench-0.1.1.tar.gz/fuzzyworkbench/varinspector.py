from tkinter import *
from tkinter.ttk import *
from fuzzyworkbench.vareditormodel import VarEditorModel, VarEditorFunction
from fuzzyworkbench.common import functionTypes, paramCount

class VarInspector(Frame):
    def __init__(self, master, editor, **kw):
        Frame.__init__(self, master, **kw)
        self._createWidgets()
        self._editor = editor
        self._var = None
        self._varSelFn = StringVar()
        
    def _createWidgets(self):
        frmForm = Frame(self)
        #Name
        Label(frmForm, text='Name:').grid(row=0, column=0, pady=10)
        self._entryName = Entry(frmForm)
        self._entryName.grid(row=0, column=1, columnspan=2, sticky='w')
        #Range
        Label(frmForm, text='Range:').grid(row=1, column=0, pady=10)
        self._spinMin = Spinbox(frmForm, from_=-1000, to=1000)
        self._spinMin.grid(row=1, column=1)
        self._spinMax = Spinbox(frmForm, from_=-1000, to=1000)
        self._spinMax.grid(row=1, column=2)
        frmForm.pack(expand=0, fill=X, pady=10)
        #Functions
        grpMembership = LabelFrame(self, text='Membership functions:')
        grpMembership.pack(expand=1, fill=BOTH, pady=10)
        self._functions = Frame(grpMembership)
        self._functions.grid_columnconfigure(2, weight=1)
        Label(self._functions, text='Name').grid(row=0, column=1, sticky='w')
        Label(self._functions, text='Type').grid(row=0, column=2, sticky='w')
        Label(self._functions, text='Params').grid(row=0, column=3, sticky='w')
        self._functions.pack(pady=10)
        frmButtonBox = Frame(grpMembership)
        self._btnAddFn = Button(frmButtonBox, text='+')
        self._btnAddFn['command'] = self._actionBtnAddFn
        self._btnDelFn = Button(frmButtonBox, text='-', state=DISABLED)
        self._btnDelFn['command'] = self._actionBtnDelFn
        self._btnDelFn.pack(side=RIGHT)
        self._btnAddFn.pack(side=RIGHT)
        frmButtonBox.pack(expand=0, fill='x')
        
    def setVar(self, var):
        self._var = var
        self._entryName['textvariable'] = var.name
        self._spinMin['textvariable'] = var.minval
        self._spinMax['textvariable'] = var.maxval
        #Remove previous functions
        cols, rows = self._functions.grid_size()
        for r in range(1, rows):
            widgets = self._functions.grid_slaves(row=r)
            for w in widgets:
                w.grid_forget()
                w.destroy()
        self._currRow = 1
        functions = self._var.getFunctions()
        createRadio = True if len(functions) > 1 else False
        for f in functions:
            self._createFnWidgets(f, createRadio)
        
    def _createFnWidgets(self, function, createRadio=True):
        #Radio
        if(createRadio):
            radio = Radiobutton(self._functions, variable=self._varSelFn)
            radio['value'] = function
            if not self._varSelFn.get():
                self._varSelFn.set(radio['value'])
            radio.grid(row=self._currRow, column=0)
        #Name
        entryName = Entry(self._functions, textvariable=function.name)
        entryName.grid(row=self._currRow, column=1)
        #Type
        box = Combobox(self._functions, values=functionTypes)
        box['textvariable'] = function.fntype
        function.fntype.trace('w', self._typeChanged)
        box.grid(row=self._currRow, column=2)
        #Params
        frmParams = Frame(self._functions)
        for i in function.getCurrParams():
            spin = Spinbox(frmParams, textvariable=i, from_=-1000, to=1000)
            spin.pack(side=LEFT, expand=1, fill=BOTH)
        frmParams.grid(row=self._currRow, column=3, sticky='we')
        self._currRow += 1    
        
    def _typeChanged(self, *args):
        self.setVar(self._var)
        
    def _actionBtnAddFn(self):
        if not self._var:
            return
        function = VarEditorFunction(self._editor, 'Z', 'triangular')
        function.setParams('triangular', (-10, 0, 10))
        self._var.addFunction(function)
        self.setVar(self._var)
        self._updateButtonSensivity()
        
    def _actionBtnDelFn(self):
        function = self._varSelFn.get() # not a function yet
        for f in self._var.getFunctions():
            if repr(f) == function:
                self._var.removeFunction(f)
        self.setVar(self._var)
        self._updateButtonSensivity()
        
    def _updateButtonSensivity(self):
        if len(self._var.getFunctions()) > 1:
            self._btnDelFn['state'] = NORMAL
        else:
            self._btnDelFn['state'] = DISABLED

if __name__ == '__main__':
    root = Tk()
    app = VarInspector(root, editor=None)
    app.pack()
    var = VarEditorModel(None, 'x', -10, 10)
    app.setVar(var)
    root.mainloop()
