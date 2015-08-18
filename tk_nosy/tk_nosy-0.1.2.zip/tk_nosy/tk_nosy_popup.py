#!/usr/bin/env python

"""
SatelliteWindow is used to display nosetests results of concurrently run
python interpreters.
"""

from __future__ import print_function
import sys
if sys.version_info < (3,):
    from future import standard_library
    standard_library.install_aliases()

#  Need to redefine object here
# pylint: disable=W0622

# pylint: disable=R0914, R0902, R0912, R0915
# pylint: disable=C0326, C0103
# pylint: disable=W0703, W0613

import tkinter.font
#from tkinter import *
from tkinter import StringVar, Label, SUNKEN, SW, X, BOTTOM, Frame, NE,\
    BOTH, TOP, Button, W, LEFT, SE, Scrollbar, VERTICAL, Text, RIGHT, Y, Tk,\
    Toplevel

class SatelliteWindow( Toplevel ):
    """
    SatelliteWindow is used to display nosetests results of concurrently run
    python interpreters.
    """

    def cleanupOnQuit(self):
        """When closing popup, do a little clean up."""
        # I'm not sure that transient windows need this, but I'm trying to be careful
        self.MainWin.focus_set()

        if self.main_gui.kill_popup_window( self.statusMessage.get() ):
            self.destroy()
            self.main_gui.statusMessage.set('Closed: ' + self.statusMessage.get())
        else:
            self.main_gui.statusMessage.set('ERROR Closing: ' + self.statusMessage.get())
        self.main_gui.set_statusbar_bg( '#FF9999' )

    def __init__(self, main_gui, MainWin, mytitle, dx=30, dy=30):
        """Initialize popup"""
        Toplevel.__init__(self, MainWin)
        self.title(mytitle)

        x = MainWin.winfo_x()
        if x<10:
            x=10
        y = MainWin.winfo_y()
        if y<10:
            y=10
        # position over to the upper right
        self.geometry( '+%i+%i'%(x+dx,y+dy))

        self.config( highlightcolor='#FF99FF', highlightbackground='#FF99FF',
                     highlightthickness=2, borderwidth=10 )

        #===========

        # make a Status Bar
        self.statusMessage = StringVar()
        self.statusMessage.set(mytitle)
        self.statusbar = Label(self, textvariable=self.statusMessage, bd=1, relief=SUNKEN)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)

        self.statusbar_bg = self.statusbar.cget('bg') # save bg for restore

        myFont = tkinter.font.Font(family="Arial", size=12, weight=tkinter.font.BOLD)
        self.statusbar.config( font=myFont )


        frame = Frame(self)
        frame.pack(anchor=NE, fill=BOTH, side=TOP)

        self.Pass_Fail_Button = Button(frame,text="Pass/Fail Will Be Shown Here",
                                       image="", width="15", background="green",
                                       anchor=W, justify=LEFT, padx=2)
        self.Pass_Fail_Button.pack(anchor=NE, fill=X, side=TOP)
        self.Pass_Fail_Button.bind("<ButtonRelease-1>", self.Pass_Fail_Button_Click)

        #self.title('%s %s.%s.%s '%(python_exe_name, python_major, python_minor, python_micro))

        self.oscillator = 1 # animates character on title
        self.oscillator_B = 0 # used to return statusbar to statusbar_bg

        self.lbframe = Frame( frame )
        self.lbframe.pack(anchor=SE, side=LEFT, fill=BOTH, expand=1)

        scrollbar = Scrollbar(self.lbframe, orient=VERTICAL)
        self.Text_1 = Text(self.lbframe, width="80", height="24", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Text_1.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Text_1.pack(side=LEFT, fill=BOTH, expand=1)

        self.resizable(1,1) # Linux may not respect this


        #===========

        self.MainWin = MainWin
        self.main_gui = main_gui

        # only main window can close this window
        self.protocol('WM_DELETE_WINDOW', self.cleanupOnQuit)

    def Pass_Fail_Button_Click(self, event):
        """Place-holder routine for user clicking Pass/Fail Button"""
        self.main_gui.Pass_Fail_Button_Click( event )


    def reset_statusbar_bg(self):
        """Return status bar to default state"""
        self.statusbar.config(bg=self.statusbar_bg)

    def set_statusbar_bg(self, c):
        """Set status bar to show new color and message"""
        self.statusbar.config(bg=c)
        self.oscillator_B = 1 # will return to initial color after a few cycles

# pylint: disable=C1001
class _Testdialog:
    """Only used to test dialog from CLI"""
    def __init__(self, master):
        """Initialize CLI test GUI"""
        frame = Frame(master, width=300, height=300)
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1

        self.Button_1 = Button(frame, text="My Popup", relief="raised", width="15")
        self.Button_1.pack()
        self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

        statframe = Frame(frame)
        master.statusMessage = StringVar()
        master.statusMessage.set('Welcome')
        self.statusbar = Label(statframe, textvariable=master.statusMessage,
                               bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
        statframe.pack(anchor=SW, fill=X, side=BOTTOM)
        self.dx = 30
        self.dy = 30

        frame.pack()

        self.dialog = None

    # pylint: disable=W0613
    def Button_1_Click(self, event): #click method for component ID=1
        """Launch Select_Py_Version for CLI testing."""
        self.dialog = SatelliteWindow(self, self.master, "Test Dialog", dx=self.dx, dy=self.dy)
        self.dx += 30
        self.dy += 30

def main():
    """Launches CLI test fixture"""
    root = Tk()
    _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
