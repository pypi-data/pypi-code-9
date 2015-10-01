from tkinter import *
from tkinter.ttk import *
from fuzzyworkbench.vareditor import VarEditor
from fuzzyworkbench.ruleseditor import RulesEditor
from fuzzyworkbench.inference import Inference
from witkets.theme import Theme

class FuzzyWorkbench(Frame):
    def __init__(self, master, **kw):
        Frame.__init__(self, master, **kw)
        self._root = master
        self._createTabs()
        
    def _createTabs(self):
        self._notebook = Notebook(self._root)
        self._editorVars = VarEditor(self._notebook)
        self._editorRules = RulesEditor(self._notebook, self)
        self._inference = Inference(self._notebook, self)
        self._notebook.add(self._editorVars, text='Variables')
        self._notebook.add(self._editorRules, text='Rules')
        self._notebook.add(self._inference, text='Inference')
        self._notebook.pack(expand=1, fill=BOTH)
        self._notebook.bind('<<NotebookTabChanged>>', self._tabChanged)
        
    def _tabChanged(self, event):
        currTab = self._notebook.index(self._notebook.select())
        #Handling rule editor real time syntax highlighting
        if currTab == 1:
            self._editorRules.enableHighlight()
        else:
            self._editorRules.disableHighlight()
        #Handling inference system
        if currTab == 2:
            self._inference.updateWidgets()
        
    def getVars(self):
        return self._editorVars.getVars()
        
    def getRules(self):
        return self._editorRules.getRules()
        
    
def main():	
    root = Tk()
    root.title('Fuzzy Workbench')
    app = FuzzyWorkbench(root)
    s = Style()
    s.theme_use('clam')
    theme = Theme(s)
    theme.setDefaultFonts()
    theme.applyDefaultTheme()
    root.mainloop()
    
if __name__ == '__main__':
    main()
