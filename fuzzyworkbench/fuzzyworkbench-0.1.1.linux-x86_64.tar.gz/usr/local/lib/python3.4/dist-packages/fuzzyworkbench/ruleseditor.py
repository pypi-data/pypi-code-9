from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from fuzzylib.ruleparser import RuleParser
from fuzzyworkbench.richtext import RuleRichText

#@TODO Highlight keywords or errors

_defaultRules = '''
IF e IS N AND de IS MN THEN u IS MP
IF e IS Z AND de IS P THEN u IS N
IF e IS P AND de IS N THEN u IS N'''.strip()

class RulesEditor(Frame):
    def __init__(self, master, app, **kw):
        Frame.__init__(self, master, **kw)
        self._compiledRules = []
        self._app = app
        frmText = Frame(self)
        self._text = RuleRichText(frmText)
        self._text['height'] = 10
        self._text.insert('1.0', _defaultRules)
        self._text.pack(side=LEFT, expand=1, fill=BOTH)
        scroll = Scrollbar(frmText)
        scroll.pack(side=RIGHT, fill=Y)
        self._text.config(yscrollcommand=scroll.set)
        scroll.config(command=self._text.yview)
        frmText.pack(expand=1, fill=BOTH, padx=10, pady=10)
        self._btnValidate = Button(self, text='Validate and Compile')
        self._btnValidate.pack()
        self._btnValidate['command'] = self.compile
        
    def enableHighlight(self):
        self._highlight = True
        self._text.after(300, self._highlightRules)
        
    def disableHighlight(self):
        self._highlight = False

    def _highlightRules(self):
        self._text.highlight_keywords()
        if self._highlight:
            self._text.after(300, self._highlightRules)
            
    def getRules(self):
        return self._compiledRules
        
    def compile(self):
        self._compiledRules = []
        rules = self._text.get("1.0", END).split('\n')
        rules = [r for r in rules if r.strip()]
        parser = RuleParser()
        for v in self._app.getVars():
            parser.add_variable(v)
        self._text.clear_errors()
        allOK = True
        for r in range(len(rules)):
            try:
                rule = parser.compile_rule(rules[r])
                self._compiledRules.append(rule)
            except:
                allOK = False
                self._text.highlight_error(r)
        if allOK:
            messagebox.showinfo('Success!', 'Rules successfully validated!')
        else:
            messagebox.showerror('Error!', 'Invalid rules detected!')
            self._compiledRules = []
        self._text.clear_errors()

if __name__ == '__main__':
    root = Tk()
    app = RulesEditor(root, None)
    app.pack()
    root.mainloop()
