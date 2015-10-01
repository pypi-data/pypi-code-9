from tkinter import *
from tkinter.ttk import *
from fuzzyworkbench.managedmodel import ManagedModel
from fuzzyworkbench.varbrowser import VarBrowser
from fuzzyworkbench.varinspector import VarInspector
from fuzzyworkbench.vareditormodel import VarEditorModel, VarEditorFunction
from fuzzyworkbench.common import functionTypes, paramCount
from fuzzylib.linguisticvar import LinguisticVar
from fuzzylib.membership import *

#@TODO Trace variables for changes
#Save button

#==============================================================================
# Editor
#==============================================================================

class VarEditor(Frame):
    def __init__(self, master, **kw):
        Frame.__init__(self, master, **kw)
        self._browser = None
        self._root = master
        self._createSidebar()
        self._createInspector()
        self._browser.select(0)
        self._inspector.setVar(self._browser.getSelected())

    def getVars(self):
        varEditorModels = self._browser.getVars()
        fuzzyVars = []
        for v in varEditorModels:
            minval, maxval = float(v.minval.get()), float(v.maxval.get())
            fuzzyVar = LinguisticVar(v.name.get(), minval, maxval)
            for f in v.getFunctions():
                fntype = f.fntype.get()
                params = [float(p.get()) for p in f.getCurrParams()]
                if fntype == 'triangular':
                    function = lambda x, p=params : triangular(x, *p)
                elif fntype == 'trapezoidal':
                    function = lambda x, p=params : trapezoidal(x, *p)
                fuzzyVar.add_set(f.name.get(), function)
            fuzzyVars.append(fuzzyVar)
        return fuzzyVars
        
    #==========================================================================
    # Creating Widgets
    #==========================================================================       
        
    def _createSidebar(self):
        sidebar = Frame(self)
        label = Label(sidebar, text='Variables')
        label.pack(expand=0)
        self._browser = VarBrowser(sidebar, self)
        self._browser.pack(expand=1, fill=Y)
        sidebar.pack(side=LEFT, expand=1, fill=Y, padx=10)
                
    def _createInspector(self):
        inspectorFrm = Frame(self)
        Label(inspectorFrm, text='Edit').pack()
        self._inspector = VarInspector(inspectorFrm, self)
        self._inspector.pack(expand=1, fill=BOTH, padx=10)
        inspectorFrm.pack(side=LEFT, expand=1, fill=BOTH)
        
    #==========================================================================
    # Handling widget changes
    #==========================================================================
    
    def notify(self, changed):
        if isinstance(changed, VarEditorModel) and self._browser:
            self._browser.updateLabels()
        elif isinstance(changed, VarBrowser) and self._browser:
            entity = self._browser.getSelected()
            self._inspector.setVar(entity)
        
    #==========================================================================
    # Handling unsaved changes
    #==========================================================================
    
    #@TODO Update title bar to show Saved/not saved
    #@TODO Prevent closing window when changes not saved
    #@TODO Prevent running inference system when changes not saved
    #@TODO Add revert functionality
    
if __name__ == '__main__':
    root = Tk()
    app = VarEditor(root)
    app.pack()
    root.mainloop()
