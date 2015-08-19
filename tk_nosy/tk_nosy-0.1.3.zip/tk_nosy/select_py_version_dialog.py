#!/usr/bin/env python
"""
Select_Py_Version is a tkinter pop-up dialog used to select a python
interpreter for use with Tk_Nosy.
"""
# pylint: disable=E0611

from __future__ import print_function
import sys
if sys.version_info < (3,):
    from future import standard_library
    standard_library.install_aliases()
    from tkSimpleDialog import Dialog
else:

    # this is only called incorrectly by pylint using python2
    from tkinter.simpledialog import Dialog

# pylint: disable=R0914, R0902, R0912, R0915
# pylint: disable=C0326, C0103
# pylint: disable=W0703, W0613

#  Need to redefine object here
# pylint: disable=W0622

#from tkinter import *
from tkinter import StringVar, Label, Frame, Button, W, Tk, Radiobutton


class _Dialog(Dialog):
    """Base class for Select_Py_Version"""
    # use dialogOptions dictionary to set any values in the dialog
    def __init__(self, parent, title=None, dialogOptions=None):
        self.initComplete = 0
        self.dialogOptions = dialogOptions
        Dialog.__init__(self, parent, title)

class Select_Py_Version(_Dialog):
    """
    Select_Py_Version is a tkinter pop-up dialog used to select a python
    interpreter for use with Tk_Nosy.
    """

    def body(self, master):
        dialogframe = Frame(master, width=300, height=300)
        dialogframe.pack()


        self.Label_1 = Label(dialogframe, text="Select Python Version")
        self.Label_1.pack()

        if self.dialogOptions:
            rbL = self.dialogOptions.get('rbL', ['No Options','No Options'])
        else:
            rbL = ['No Options', 'No Options']

        self.RadioGroup1_StringVar = StringVar()
        self.RadioGroup1_StringVar.set(rbL[0])
        self.RadioGroup1_StringVar_traceName = \
            self.RadioGroup1_StringVar.trace_variable("w", self.RadioGroup1_StringVar_Callback)

        for rb in rbL:
            self.Radiobutton_1 = Radiobutton(dialogframe, text=rb, value=rb)
            self.Radiobutton_1.pack(anchor=W)
            self.Radiobutton_1.configure( variable=self.RadioGroup1_StringVar )
        self.resizable(0, 0) # Linux may not respect this


    def RadioGroup1_StringVar_Callback(self, varName, index, mode):
        """When radio group selection changes, print message to CLI."""
        print( "RadioGroup1_StringVar_Callback varName, index, mode",
                varName, index, mode )
        print( "    new StringVar value =", self.RadioGroup1_StringVar.get() )


    def validate(self):
        """Validates and packages dialog selections prior to return to calling
           routine.
           set values in "self.result" dictionary for return
        """
        self.result = {} # return a dictionary of results

        self.result["selection"] = self.RadioGroup1_StringVar.get()
        return 1

    def apply(self):
        print( 'apply called')

# pylint: disable=C1001
class _Testdialog:
    """Only used to test dialog from CLI"""
    def __init__(self, master):
        """Initialize CLI test GUI"""
        frame = Frame(master, width=300, height=300)
        frame.pack()
        self.master = master
        self.x, self.y, self.w, self.h = -1, -1, -1, -1

        self.Button_1 = Button(text="Test Dialog", relief="raised", width="15")
        self.Button_1.place(x=84, y=36)
        self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

    def Button_1_Click(self, event): #click method for component ID=1
        """Launch Select_Py_Version for CLI testing."""
        rbL = ['2.5.5', '2.6.6', 'PYPY 3.2.2']
        dialog = Select_Py_Version(self.master, "Test Dialog", dialogOptions={'rbL':rbL})
        print( '===============Result from Dialog====================' )
        print( dialog.result)
        print( '=====================================================' )

def main():
    """Launches CLI test fixture"""
    root = Tk()
    _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
