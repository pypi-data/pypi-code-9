from math import pi
from tkinter import *
from tkinter.ttk import *
from fuzzyworkbench.entitybrowser import EntityBrowser
from fuzzyworkbench.vareditormodel import VarEditorModel, VarEditorFunction

_sampleVars = {
    ('e', -pi/4, pi/4) : [
        ('N', 'trapezoidal', (-100, -90, -pi/4, 0)),
        ('Z', 'triangular', (-pi/4, 0, pi/4)),
        ('P', 'trapezoidal', (0, pi/4, 90, 100))
    ],
    ('de', -pi/4, pi/4) : [
        ('MN', 'trapezoidal', (-100, -90, -pi/4, -pi/8)),
        ('N', 'triangular', (-pi/4, -pi/8, 0)),
        ('Z', 'triangular', (-pi/8, 0, pi/8)),
        ('P', 'triangular', (0, pi/8, pi/4)),
        ('MP', 'trapezoidal', (pi/8, pi/4, 90, 100)),
    ],
    ('u', -30, 30) : [
        ('MN', 'triangular', (-30, -20, -10)),
        ('N', 'triangular', (-20, -10, 0)),
        ('Z',  'triangular', (-10, 0, 10)),
        ('P', 'triangular', (0, 10, 20)),
        ('MP', 'triangular', (10, 20, 30))
    ]
}

class VarBrowser(EntityBrowser, Frame):
    def __init__(self, master, editor, **kw):
        Frame.__init__(self, master, **kw)
        EntityBrowser.__init__(self, editor)
        #Widgets
        self.grid_rowconfigure(0, weight=1)
        self._list = Listbox(self)        
        self._list['selectmode'] = SINGLE
        self._list['exportselection'] = False
        self._btnAdd = Button(self, text='+')
        self._btnAdd['command'] = self._actionBtnAdd
        self._btnDel = Button(self, text='-')
        self._btnDel['command'] = self._actionBtnDel
        #Layout
        self._list.grid(row=0, column=0, columnspan=2, sticky='NS')
        self._btnAdd.grid(row=1, column=0)
        self._btnDel.grid(row=1, column=1)
        #First variable
        self._createSampleVars()
        #Events
        self._list.bind('<<ListboxSelect>>', self._selChanged)
        
    def _createSampleVars(self):
        for var, functions in _sampleVars.items():
            v = VarEditorModel(self._editor, var[0], var[1], var[2])
            for function in functions:
                f = VarEditorFunction(self._editor, function[0], function[1])
                f.setParams(function[1], function[2])
                v.addFunction(f)
            self.add(v)
        self._updateButtonSensivity()
        
                
    # =========================================================================
    # Buttons
    # =========================================================================
        
    def _actionBtnAdd(self):
        var = VarEditorModel(self._editor, 'v1', -10, 10)
        function = VarEditorFunction(self._editor, 'Z', 'triangular')
        function.setParams('triangular', (-10, 0, 10))
        var.addFunction(function)
        self.add(var)
        self._updateButtonSensivity()
        
    def _actionBtnDel(self):
        if self._list.size() > 1:
            self.remove(self.getSelected())
        self._updateButtonSensivity()
        
    def _updateButtonSensivity(self):
        if self._list.size() > 1:
            self._btnDel['state'] = NORMAL
        else:
            self._btnDel['state'] = DISABLED
            
    # =========================================================================
    # Events
    # =========================================================================
        
    def _selChanged(self, event=None):
        if self._editor:
            self._editor.notify(self)
        
    def updateLabels(self):
        currEntity = self.getSelected()
        if not currEntity:
            return
        self._list.delete(0, END)
        for e in self._entities:
            self._list.insert(END, str(e))
        self.select(currEntity)

    # =========================================================================
    # Actions
    # =========================================================================
                
    def add(self, entity):
        EntityBrowser.add(self, entity)
        self._list.insert(END, str(entity))
        self.select(entity)
        
    def remove(self, entity):
        idx = self._entities.index(entity)
        self._list.delete(idx)
        EntityBrowser.remove(self, entity)
        self.select(self._entities[0])
        
    def select(self, entity):
        self._list.selection_clear(0, END)
        if not isinstance(entity, int):
            entity = self._entities.index(entity)
        self._list.selection_set(entity)
        self._selChanged()
        
    def getSelected(self):
        idx = self._list.curselection()
        if idx:
            return self._entities[idx[0]]
        return None
        
    def size(self):
        return self._list.size()
        
    def getVars(self):
        return self._entities
        
if __name__ == '__main__':
    root = Tk()
    app = VarBrowser(root, None)
    app.pack()
    root.mainloop()
