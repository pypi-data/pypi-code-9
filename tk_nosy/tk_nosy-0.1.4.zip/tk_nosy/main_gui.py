
"""
Watch for changes in all .py files. If changes, run nosetests.
"""
from __future__ import absolute_import
from __future__ import print_function
import sys
if sys.version_info < (3,):
    from future import standard_library
    standard_library.install_aliases()
    import tkFileDialog
    import tkMessageBox
else:
    import tkinter.filedialog as tkFileDialog
    import tkinter.messagebox as tkMessageBox

#  Need to redefine object here
# pylint: disable=W0622, W0703, W0612, W0403, C0330
from builtins import object

import tkinter.font
#from tkinter import *
from tkinter import Menu, StringVar, Label, SUNKEN, SW, X, BOTTOM, Frame, NE,\
    BOTH, TOP, Button, W, LEFT, SE, Scrollbar, VERTICAL, Text, RIGHT, Y, END, Tk

#import nose
#print( 'nose.__file__ =',nose.__file__ )
#print( ' sys.executable =', sys.executable)

from xml.etree import ElementTree as ET

import stat
import os, fnmatch

# Man this is ugly... It's only used during development (prior to running
#   setup.py install) After installed, the tk_nosy.xxxx should succeed for 2&3
try:
    from tk_nosy.pyterps import PyInterpsOnSys, get_nose_version_info
    from tk_nosy.select_py_version_dialog import Select_Py_Version
    from tk_nosy.tk_nosy_popup import SatelliteWindow
except:
    from pyterps import PyInterpsOnSys, get_nose_version_info
    from select_py_version_dialog import Select_Py_Version
    from tk_nosy_popup import SatelliteWindow

# pylint: disable=R0914, R0902, R0912, R0915

LICENSE = """
tk_nosy  Copyright (C) 2013-2015  Charlie Taylor
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""


__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2013 Charlie Taylor'
__license__ = 'GPL-3'  # see file LICENSE.TXT
__version__ = '0.1.4'  # METADATA_RESET:__version__ = '<<version>>'
__email__ = "charlietaylor@users.sourceforge.net"
__status__ = "Development"  # "Prototype", "Development", or "Production"


#    I like extra spaces inside parens and sometimes camelCase
# pylint: disable=C0326
# pylint: disable=C0103

fileD = {} # key=file name, value=(size, modified time)
changedFileL = []

def walkLocate(pattern, topDir=os.curdir):
    """Locate all files matching supplied filename pattern in and below
    supplied topDir directory."""
    # pylint: disable=W0612
    for path, _dirL, fileL in os.walk(os.path.abspath(topDir)):

        if '.tox' in path.split(os.sep):
            #print 'Skipping',path
            continue
        for filename in fnmatch.filter(fileL, pattern):
            yield os.path.join(path, filename)

def numberOfChangedFiles( dirname ):
    """ Return number of .py files that have changed since last check."""
    del changedFileL[:]
    numFilesChanged = 0
    numFilesExamined = 0
    for f in walkLocate('*.py', topDir=dirname):
        numFilesExamined += 1
        size, mtime = fileD.get(f,(0,0))
        stats = os.stat (f)
        sizeNow, mtimeNow = stats[stat.ST_SIZE], stats[stat.ST_MTIME]
        if size!=sizeNow or mtime!=mtimeNow:
            numFilesChanged += 1
            changedFileL.append( f )
        fileD[f] = (sizeNow, mtimeNow)

    if numFilesExamined != len(fileD): # new or deleted file
        numFilesChanged += abs(numFilesExamined - len(fileD))
        fileD.clear()
    return numFilesChanged

def ShowWarning(title='Title', message='your message here.'):
    """Simply wraps the tkinter function of the "same" name."""
    tkMessageBox.showwarning( title, message )
    return
def ShowError(title='Title', message='your message here.'):
    """Simply wraps the tkinter function of the "same" name."""
    tkMessageBox.showerror( title, message )
    return

def run_nosetests(numNosyCalls, PI, display_test_details='Y'):
    """Run nosetests, create xml file of output, parse the xml file
       to determine the results.

       Return the results to the calling method.

       :param numNosyCalls: counter for total runs of nosetests
       :type numNosyCalls: int
       :param PI: PyInterp object holding information of which python interpreter
                  to run nosetests with
       :type PI: object
    """

    #print("Path at terminal when executing this file")
    #print("    " + os.getcwd() + "\n")

    xml_filename = 'nosetests_%s.xml'%PI.name().replace(' ','')
    #os.system (full_nosetests_name + ' --with-xunit  --xunit-file=%s'%xml_filename)
    
    code = """import sys;from nose import run_exit;sys.exit(run_exit(argv=[ '', '--with-xunit', '--xunit-file=%s']))"""%xml_filename
    
    cmd = '''%s -c "%s"'''%(PI.full_path, code)

    os.system ( cmd )
    

    #print 'system_rtn = ',system_rtn
    #system_rtn = nose.run( argv=['nosetests', '-v', '--with-xunit'])
    #system_rtn = nose.main(argv=['nosetests', '-v', '--with-xunit'])

    #s = 'UNITTEST RUN# %i'%numNosyCalls
    s = 'tk_nosy UNITTEST RUN# %i'%numNosyCalls
    outputTextL = [ s.center(40,'_') + '\n\n']

    tree = ET.parse(xml_filename)

    # clean up xml file after each use.
    os.remove( xml_filename )

    numFailed = 0
    numErrors = 0
    numSkipped = 0
    numTests = 0

    for e in tree.getiterator('testsuite'):
        #print '%i)'%ie,e.items()
        numErrors += int( e.get('errors',0) )
        numFailed += int( e.get('failures',0) )
        numSkipped += int( e.get('skip',0) )
        numTests += int( e.get('tests',0) )

    numPassed = numTests - numFailed - numErrors - numSkipped
    passedAllTests = (numTests - numSkipped == numPassed) and (numFailed==0) and (numErrors==0)

    # Make outputTextL that will be displayed in Text_1 window
    iText = 1
    for testcase in tree.getiterator('testcase'):
        #print 'len(testcase)=',len(testcase)

        label = ''
        if len(testcase) > 0:
            title = "{Item #%i} "%iText + testcase.get('name','')

            ssL = []
            for  child in testcase:
                if not label:
                    label = child.get('type','')

                sL = child.text.strip().split('\n')
                for isL,s in enumerate(sL):
                    sL[isL] = s.rstrip()

                ssL.append( sL )
                print()
            print(title + ', %s'%label)
            outputTextL.append( title + ', %s'%label + '\n' )
            for sL in ssL:
                #print '\n'.join(sL)
                outputTextL.append( '\n'.join(sL) + '\n\n' )
            iText += 1

    if (display_test_details=='N') and passedAllTests:
        outputTextL = ['Passed All Tests\n\n']
    return passedAllTests, numPassed, numFailed, numErrors, numSkipped, outputTextL



class Tk_Nosy(object):
    """This class is the tkinter GUI object"""

    # make a collection of python interpreters to choose from
    pythonInterpreterCollection = None # will be PyInterpsOnSys object

    # extra python interpreters can run nosetests concurrently to main window
    #  concurrent_versionL contains tuples = (PI, Popup)
    concurrent_versionL = [] # additional running python interpreters


    def __init__(self, master):
        self.dirname = os.path.abspath( os.curdir )

        self.initComplete = 0
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1

        # bind master to <Configure> in order to handle any resizing, etc.
        # postpone self.master.bind("<Configure>", self.Master_Configure)
        self.master.bind('<Enter>', self.bindConfigure)

        self.menuBar = Menu(master, relief = "raised", bd=2)

        self.menuBar.add("command", label = "Change_Dir", command = self.menu_Directory_Change_Dir)

        disp_Choices = Menu(self.menuBar, tearoff=0)
        self.display_test_details = StringVar()
        self.display_test_details.set('Y')
        disp_Choices.add_checkbutton(label='Display Test Details', variable=self.display_test_details, onvalue='Y', offvalue='N')
        
        self.display_watched_files = StringVar()
        self.display_watched_files.set('Y')
        disp_Choices.add_checkbutton(label='Show Watched Files', variable=self.display_watched_files, onvalue='Y', offvalue='N')
        self.menuBar.add("cascade", label="Display", menu=disp_Choices)
                          
                          
        py_choices = Menu(self.menuBar, tearoff=0)
        py_choices.add("command", label = "Change Python Version",
                          command = self.changePythonVersion)
        py_choices.add("command", label = "Find New Python Interpreter",
                          command = self.findNewPythonInterpreter)
        py_choices.add("command", label = "Launch Another Python Interpreter",
                          command = self.launchAnotherPythonInterpreter)
        self.menuBar.add("cascade", label="Python", menu=py_choices)


        #top_Snippet = Menu(self.menuBar, tearoff=0)

        self.menuBar.add("command", label = "Run", command = self.menu_Run)
        
        self.display_test_details.trace("w", self.rerun_tests)
        self.display_watched_files.trace("w", self.rerun_tests)

        master.config(menu=self.menuBar)

        # make a Status Bar
        self.statusMessage = StringVar()
        self.statusMessage.set(self.dirname)
        self.statusbar = Label(self.master, textvariable=self.statusMessage,
                               bd=1, relief=SUNKEN)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)

        self.statusbar_bg = self.statusbar.cget('bg') # save bg for restore

        self.arial_12_bold_font = tkinter.font.Font(family="Arial", size=12,
                                                    weight=tkinter.font.BOLD)
        self.arial_12_font      = tkinter.font.Font(family="Arial", size=12)


        self.statusbar.config( font=self.arial_12_bold_font )

        frame = Frame(master)
        frame.pack(anchor=NE, fill=BOTH, side=TOP)

        self.Pass_Fail_Button = Button(frame,text="Pass/Fail Will Be Shown Here",
                                       image="", width="15", background="green",
                                       anchor=W, justify=LEFT, padx=2)
        self.Pass_Fail_Button.pack(anchor=NE, fill=X, side=TOP)
        self.Pass_Fail_Button.bind("<ButtonRelease-1>", self.Pass_Fail_Button_Click)

        self.master.title("tk_nosy")

        self.oscillator = 1 # animates character on title
        self.oscillator_B = 0 # used to return statusbar to statusbar_bg

        self.lbframe = Frame( frame )
        self.lbframe.pack(anchor=SE, side=LEFT, fill=BOTH, expand=1)

        scrollbar = Scrollbar(self.lbframe, orient=VERTICAL)
        self.Text_1 = Text(self.lbframe, width="80", height="24",
                           yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Text_1.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Text_1.pack(side=LEFT, fill=BOTH, expand=1)

        self.master.resizable(1,1) # Linux may not respect this

        self.numNosyCalls = 0
        self.need_to_pick_dir = 1

        print('sys.argv =',sys.argv)
        if len(sys.argv)>1:
            #  I don't care what the exception is, if there's a problem, bail
            # pylint: disable=W0702
            print( "Try Dir =",sys.argv[1] )
            try:
                dirname = os.path.abspath( sys.argv[1] )
                self.try_change_to_new_dir( dirname )
            except Exception:
                pass # let Alarm force dir selection
        else:
            try:
                if os.path.isdir(os.path.join( self.dirname, 'tests' )):
                    self.try_change_to_new_dir( self.dirname )
            except Exception:
                pass # let Alarm force dir selection


        print(LICENSE)

        self.defaultPyInterp = None # need to identify default python interpreter
        if Tk_Nosy.pythonInterpreterCollection == None:
            Tk_Nosy.pythonInterpreterCollection = PyInterpsOnSys()
            self.defaultPyInterp = Tk_Nosy.pythonInterpreterCollection.get_PI_obj_by_py_path( sys.executable )
            #print( Tk_Nosy.pythonInterpreterCollection )

        self.Alarm()


    def try_change_to_new_dir(self, dirname):
        """A legal abspath will switch to dirname."""
        #  I don't care what the exception is, if there's a problem, bail
        # pylint: disable=W0702
        if dirname:
            try:
                dirname = os.path.abspath( dirname )
            except:
                return # let Alarm force dir selection
        else:
            return

        self.dirname = dirname
        print('Selected dirname    =',dirname)
        fileD.clear()
        os.chdir( self.dirname )
        self.reset_statusbar_bg()
        self.need_to_pick_dir = 0

        #with open(NOSY_USER_DATA_FILE, 'w') as text_file:
        #    text_file.write( self.dirname )

        self.numNosyCalls = 0


    def reset_statusbar_bg(self):
        """Return status bar to default state"""
        self.statusbar.config(bg=self.statusbar_bg)
        self.statusMessage.set(self.dirname)

    def set_statusbar_bg(self, c):
        """Set status bar to show new color and message"""
        self.statusbar.config(bg=c)
        self.oscillator_B = 1 # will return to initial color after a few cycles

    def menu_Directory_Change_Dir(self):
        """Menu selection to set directory in which to run nosetests"""
        dirname = self.AskDirectory( title='Choose Directory For Nose Tests', initialdir=".")
        if dirname:
            self.try_change_to_new_dir( dirname )
        # >>>>>>insert any user code below this comment for section "menu_Directory_Change_Dir"
        # replace, delete, or comment-out the following
        print("called menu_Directory_Change_Dir")


    def menu_Run(self):
        """User initiates a nosetests run, not file change detection."""
        print("called menu_Run")
        self.callNosy()
    def rerun_tests(self,*args):
        self.menu_Run()


    def callNosy(self):


        """Run nosetests and display results"""
        self.numNosyCalls += 1

        runL = [(self.defaultPyInterp, self)]
        for PI,Popup in Tk_Nosy.concurrent_versionL:
            runL.append( (PI, Popup) )

        for PI, tkwindow in runL:
            tkwindow.Text_1.delete(1.0, END)

            # turn indicator button gray while running the tests
            tkwindow.Pass_Fail_Button.config(background="#999999",
                                             text='TESTING...',
                                             font=self.arial_12_bold_font)
        self.master.update()
        self.master.update_idletasks()

        for PI, tkwindow in runL:
            self.run_tkwin_nosetests( PI, tkwindow)

        self.master.winfo_toplevel().wm_geometry("")



    def run_tkwin_nosetests(self, PI, tkwindow):
        """Run nosetests for main python interpreter and any concurrent
             python interpreters.

           Update GUI to show results.
        """
        
        if PI.nose_version == None:
            # if nose was not installed last time we checked, check again
            PI.nose_version, err_msg = get_nose_version_info( PI.full_path )
            if PI.nose_version == None:
                print( "\a" )  # make beep
                s = 'Can not verify nose for:\nPython ' + PI.name()
                tkwindow.Pass_Fail_Button.config(background='orange', 
                                                  text=s, 
                                                  font=self.arial_12_bold_font)
                s = 'Please verify nose installed for:\n'+str(PI) +\
                    '\n\n' + err_msg+\
                    '\n\nFor install instructions see:\n'+\
                    'https://nose.readthedocs.org/en/latest/'
                tkwindow.Text_1.insert(END, s )
                ShowError(title='Can not verify nose', message=s)
                return
        
        # pylint: disable=W0201
        passedAllTests, numPassed, numFailed, numErrors, numSkipped, outputTextL = \
            run_nosetests(self.numNosyCalls, PI, display_test_details=self.display_test_details.get())

        max_len_s = 42
        num_lines = 1
        for s in outputTextL:
            tkwindow.Text_1.insert(END, s)
            sL = s.split('\n')
            for ss in sL:
                max_len_s = max(max_len_s, len(ss))
                num_lines += 1


        if self.numNosyCalls % 2:
            myFont = self.arial_12_bold_font
        else:
            myFont = self.arial_12_font

        if passedAllTests:
            s = 'PASSED'
            if numPassed > 1:
                s = 'PASSED ALL %i TESTS'%numPassed
            elif numPassed == 1:
                s = 'PASSED ONE TEST'


            bg="#00ff00"
            if numSkipped==1:
                s = 'passed with 1 SKIP'
                bg = "#00cc00"
            elif numSkipped > 1:
                s = 'passed with %i SKIPS'%numSkipped
                bg = "#00cc00"
            elif numPassed==0:
                s = 'No Tests Found'
                bg="#ff8000"
            tkwindow.Pass_Fail_Button.config(background=bg, text=s, font=myFont)

            #self.master.geometry('200x50')
        else:
            s = 'FAILED %i, ERRORS %i, SKIP %i, PASSED %i'%(numFailed,
                                                            numErrors, numSkipped, numPassed)
            tkwindow.Pass_Fail_Button.config(background="#ff0000", text=s, font=myFont)
            #self.master.geometry('516x385')


        # Show list of files being watched.
        #self.Text_1.insert(END, '_'*40+'\n')
        tkwindow.Text_1.insert(END, 'WATCHED *.py FILES'.center(40,'_') + '\n' )
        tkwindow.Text_1.insert(END, '%s%s..\n\n'%(self.dirname,os.path.sep) )
        num_lines += 3

        len_dirname = len( self.dirname )
        
        if self.display_watched_files.get()=='Y':
            keyL = list(fileD.keys())
            keyL.sort()
            lastdir = ''
            for key in keyL:
                dn = os.path.dirname( key )
                if dn != lastdir:
                    tkwindow.Text_1.insert(END, '..'+dn[len_dirname:] + '\n')
                    max_len_s = max(max_len_s, len(dn)+1)
                    lastdir = dn
                    num_lines += 1
                s = '    ' +os.path.basename( key )
                tkwindow.Text_1.insert(END, s + '\n')
                max_len_s = max(max_len_s, len(s)+1)
                num_lines += 1
        else:
            num_lines += 1
            tkwindow.Text_1.insert(END, '     %i files watched.\n'%len(fileD))

        tkwindow.Text_1.config(width=max_len_s)
        tkwindow.Text_1.config(height=min(40, num_lines))


    def bindConfigure(self, event):
        """Part of goofy main window setup in tkinter."""
        #  tkinter requires arguments, but I don't use them
        # pylint: disable=W0613
        if not self.initComplete:
            self.master.bind("<Configure>", self.Master_Configure)
            self.initComplete = 1

    def change_python_exe(self, full_path ):
        """Allow nosetests to be run under any available python version """
        PI = Tk_Nosy.pythonInterpreterCollection.add_interp( full_path )
        if PI:
            self.defaultPyInterp = PI


    def findNewPythonInterpreter(self):
        """Find a new python interpreter, one that is not already in
             the PyInterpsOnSys object (pythonInterpreterCollection).
        """
        if Tk_Nosy.pythonInterpreterCollection == None:
            print( 'pythonInterpreterCollection NOT yet initialized' )
            self.statusMessage.set('Interpreter Collection NOT initialized')
            self.set_statusbar_bg( '#FF9999' )
            return

        print('Open File')
        filetypes = [
            ('python executable','py*'),
            ('Any File','*.*')]
        pathopen = tkFileDialog.askopenfilename(parent=self.master,
                       title='Select Python Executable',
                       filetypes=filetypes,
                       initialdir=self.defaultPyInterp.full_path)

        if pathopen:
            self.change_python_exe( pathopen )
            self.menu_Run()

    def kill_popup_window(self, popup_name):
        """Close a popup window running another verions of python interpreter"""
        for itup, tup in enumerate(Tk_Nosy.concurrent_versionL):
            PI, Popup = tup
            s = '%s %s' % (PI.exe_name, PI.version_str)
            if popup_name == s:
                Tk_Nosy.concurrent_versionL.pop( itup )
                return True # removed popup from list
        return False # no popup found


    def launchAnotherPythonInterpreter(self):
        """Launch a pop-up window that concurrently runs another python version"""

        removeNameL=[self.defaultPyInterp.name()]
        for PI,Popup in Tk_Nosy.concurrent_versionL:
            removeNameL.append( PI.name() )

        piL = Tk_Nosy.pythonInterpreterCollection.get_PI_list( removeNameL=removeNameL )
        if len(piL)==0:
            print( 'All identified python interpreters in use.' )
        else:
            print( [pi.name() for pi in piL] )
            rbL = [PI.name() for PI in piL]
            dialog = Select_Py_Version(self.master, "Launch Another Python Version",
                                       dialogOptions={'rbL':rbL})
            if dialog.result:
                PI = Tk_Nosy.pythonInterpreterCollection.get_PI_obj_by_name(
                                                    dialog.result['selection'])

                s = '%s %s' % (PI.exe_name, PI.version_str)
                Popup = SatelliteWindow(self, self.master, s)
                Tk_Nosy.concurrent_versionL.append( (PI, Popup) )
                self.menu_Run()

    def changePythonVersion(self):
        """Change to a different python version.
           If the PyInterpsOnSys object (pythonInterpreterCollection) has been
           initialized, select from its list.
           Otherwise find the python interpreter executable
           (ex. python.exe or python)
        """
        if (Tk_Nosy.pythonInterpreterCollection == None) or \
           (Tk_Nosy.pythonInterpreterCollection.num_terps() == 0):
            # If there is no list of available python interpreters, look for python file
            print('Open File')
            filetypes = [
                ('python executable','py*'),
                ('Any File','*.*')]
            pathopen = tkFileDialog.askopenfilename(parent=self.master,
                           title='Select Python Executable',
                           filetypes=filetypes,
                           initialdir=self.defaultPyInterp.full_path)

            if pathopen:
                self.change_python_exe( pathopen )
                self.menu_Run()
        else:
            rbL = [PI.name() for PI in Tk_Nosy.pythonInterpreterCollection.interpL]
            dialog = Select_Py_Version(self.master, "Select Python Version",
                                       dialogOptions={'rbL':rbL})
            if dialog.result:
                PI = Tk_Nosy.pythonInterpreterCollection.get_PI_obj_by_name(
                                                   dialog.result['selection'] )
                pathopen = PI.full_path

                self.change_python_exe( pathopen )
                self.menu_Run()

    # return a string containing directory name
    def AskDirectory(self, title='Choose Directory', initialdir="."):
        """Run pop-up menu for user to select directory."""
    #    This is not an error
    # pylint: disable=E1101

        if sys.version_info < (3,):
            dirname = tkFileDialog.askdirectory(parent=self.master,
                                             initialdir=initialdir,title=title)
        else:
            dirname = tkFileDialog.askdirectory(parent=self.master,
                                             initialdir=initialdir,title=title)
        return dirname # <-- string


    def Master_Configure(self, event):
        """Part of tkinter main window initialization"""

        if event.widget != self.master:
            if self.w != -1:
                return
        x = int(self.master.winfo_x())
        y = int(self.master.winfo_y())
        w = int(self.master.winfo_width())
        h = int(self.master.winfo_height())
        if (self.x, self.y, self.w, self.h) == (-1,-1,-1,-1):
            self.x, self.y, self.w, self.h = x,y,w,h


        if self.w!=w or self.h!=h:
            #print "Master reconfigured... make resize adjustments"
            self.w=w
            self.h=h

    # pylint: disable=W0613
    def Pass_Fail_Button_Click(self, event):
        """Routine for user clicking Pass/Fail Button"""
        print('Arranging Windows by User Request')
        num_popups = len(Tk_Nosy.concurrent_versionL)
        DX = 50
        DY = 70
        x = 10
        y = 10 + num_popups * DY
        self.master.geometry( '+%i+%i'%(x,y))

        for PI,Popup in Tk_Nosy.concurrent_versionL:
            x += DX
            y -= DY
            Popup.geometry( '+%i+%i'%(x,y))



    # alarm function is called after specified number of milliseconds
    def SetAlarm(self, milliseconds=1000):
        """Reinitialize tkinter alarm mechanism as well as update seconds
           counter in main window title bar.
        """
        self.master.after( milliseconds, self.Alarm )

        self.oscillator += 1
        if self.oscillator > 5:
            self.oscillator = 0

        if self.oscillator_B>0:
            self.oscillator_B += 1
        if self.oscillator_B>5:
            self.oscillator_B = 0
            self.reset_statusbar_bg()

        pad = '|'*self.oscillator

        s = '%s (v%s)'%(self.defaultPyInterp.exe_name, self.defaultPyInterp.version_str)

        self.master.title('%i) %s '%(self.numNosyCalls , s + pad ))

        for PI,Popup in Tk_Nosy.concurrent_versionL:
            s = '%s (v%s)'%(PI.exe_name, PI.version_str)
            Popup.title( '%i) %s '%(self.numNosyCalls , s + pad ) )



    def Alarm(self):
        """Look for changed files every second, then reset alarm"""
        if self.need_to_pick_dir:
            dirname = self.AskDirectory( title='Choose Directory For Nose Tests', initialdir=".")
            self.try_change_to_new_dir( dirname )

        #first call to numberOfChangedFiles will be > 0 if any .py files are found
        elif numberOfChangedFiles( self.dirname ) > 0: # or self.numNosyCalls==0
            self.callNosy()

        self.SetAlarm()

def main():
    """Run Main Window"""
    root = Tk()
    Tk_Nosy(root)
    root.mainloop()


if __name__ == '__main__':
    main()
