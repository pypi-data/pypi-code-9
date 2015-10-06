# ezdialog.py - Mike Callahan - Python 2.7 - 09/21/2015
# Makes it easy to create guis, dialogs, and message windows
#
# History:
# 1.00 - initial version
# 1.01 - make master, title an optional parameter
# 1.10 - major rewrite
# 1.20 - add spin blank assignment
# 1.21 - fix spinbox null seperator bug
# 1.30 - add notebook to get and setParameters, remove autogridding for EzMessage
# 1.31 - rename message._exit to close to expose method, change font for EzMessage
# 1.32 - fix treelist scrolling, setParameter
# 1.40 - add makeText; add worient to all widgets; clean up getParameter, setParameter
# 1.41 - fix getParameter for spin
# 1.50 - add catchExcept, makeOption for EzDialog;
# 1.51 - fix _addrow
###################################################################

try:
    import Tkinter as tk                               # support Python 2
except ImportError:
    import tkinter as tk                               # support Python 3
import time, ttk, sys, warnings, tkFont
from tkFileDialog import askopenfilename, asksaveasfilename

class EzDialog(tk.Frame):
    """ easy dialog window creator """

    def __init__(self, master=None, worient='vertical'):
        """ set-up window and create result dictionary
        master:tk.Toplevel - toplevel window
        worient:str - orient of widgets; vertical or horizontal """
        self.worient = worient
        tk.Frame.__init__(self, master)                # create frame
        self.result = {}                               # frame must manually grid
        top = self.winfo_toplevel()
        if 'destroy' in top.protocol(name='WM_DELETE_WINDOW'): # set close window to _cancel
            top.protocol(name='WM_DELETE_WINDOW', func=self._cancel)

    def __getitem__(self, row):
        """ support indexed retreival
        row:int - widget row """
        return self.getParameter(row)                  # support value = dialog[row]

    def __setitem__(self, row, value):
        """ support indexed assignment
        row:int - widget row
        value:object - assignment object """
        self.setParameter(row, value)                  # support dialog[row] = value

    def setTitle(self, prompt):
        """ set the title for a window
        prompt:str - the title """
        self.master.title(prompt)

    def makeLabel(self, rowcol, init='', style='', gap=3):
        """ create a label
        rowcol:int - row or column number
        init:str - label text
        style:string - 'bold' and/or 'italic'
        gap:int - space between widgets
        -> ttk.Label """
        self.result[rowcol] = ['label', tk.StringVar()] # init result to tk var
        label = ttk.Label(self, textvariable=self.result[rowcol][1]) # create label
        self.result[rowcol][1].set(init)               # set the init value
        font = label['font']                           # get the current font
        font = tkFont.Font(family=font)                # break it down
        weight = 'bold' if 'bold' in style else 'normal' # set weight
        slant = 'italic' if 'italic' in style else 'roman' # set slant
        font.configure(weight=weight, slant=slant)     # change weight, slant
        label['font'] = font                           # use it
        if self.worient == 'vertical':
            label.grid(row=rowcol, column=0, pady=gap) # grid it
        else:                                          # 'horizontal'
            label.grid(row=0, column=rowcol, padx=gap)
        return label

    def makeLine(self, rowcol, gap=3):
        """ create a horizontal or vertical line
        rowcol:int - row number
        gap:int - space between widget frames
        -> ttk.Separator """
        if self.worient == 'horizontal':
            line = ttk.Separator(self, orient='horizontal') # create line
            line.grid(row=rowcol, column=0, sticky='we', pady=gap) # stretch across frame
        else:
            line = ttk.Separator(self, orient='vertical')
            line.grid(row=0, column=rowcol, sticky='ns', padx=gap)
        return line

    def makeEntry(self, rowcol, width, prompt, gap=3):
        """ create an Entry Box
        rowcol:int - row or column number
        width:int - width of entry widget
        prompt:str - text of frame label
        gap:int - space between widget frames
        -> ttk.Entry """
        self.result[rowcol] = ['entry', tk.StringVar()] # init result to tk var
        frame = ttk.LabelFrame(self, text=prompt)      # create titled frame
        entry = ttk.Entry(frame, width=width, textvariable=self.result[rowcol][1]) #create entry
        entry.grid(sticky='w')                         # grid entry
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return entry

    def makeCombo(self, rowcol, width, prompt, alist=[], gap=3):
        """ create a combobox which can be dynamic
        rowcol:int - row or column number
        width:int - width of entry widget
        prompt:str - text of frame label
        alist:list - items in pulldown
        gap:int - space between widget frames
        -> ttk.Comobox """
        self.result[rowcol] = ['combo', tk.StringVar()]
        frame = ttk.LabelFrame(self, text=prompt)
        combobox = ttk.Combobox(frame, width=width, textvariable=self.result[rowcol][1],
            values=alist)                              # create combobox
        combobox.grid(sticky='w')                      # grid combobox
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return combobox

    def makeChecks(self, rowcol, width, prompt, alist, orient='horizontal', gap=3):
        """ create a series of checkbuttons
        rowcol:int - row or column number
        width:int - width of entry widget
        prompt:str - text of frame label
        alist:list - items in pulldown
        orient:str - 'horizontal' or 'vertical'
        gap:int - space between widget frames
        -> [ttk.Checkbuttons] """
        self.result[rowcol] = ['checks', {}]           # init result to dict
        frame = ttk.LabelFrame(self, text=prompt)
        cbuttons = []                                  # list for checkbuttons
        for n, item in enumerate(alist):               # for every item in the given list
            temp = tk.BooleanVar()                     # create the booleanvar
            self.result[rowcol][1][item] = temp           # set boolean into result
            checkbutton = ttk.Checkbutton(frame, width=width, variable=temp,
                text=item)                             # create checkbutton
            if orient == 'vertical':
                checkbutton.grid(row=n, column=0)      # grid it
            else:
                checkbutton.grid(row=0, column=n)
            cbuttons.append(checkbutton)               # add checkbutton to list
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return cbuttons                                # list of checkbuttons

    def makeRadios(self, rowcol, width, prompt, alist, orient='horizontal', gap=3):
        """ create a series of radiobuttons
        rowcol:int - row or column number
        width:int - width of entry widget
        prompt:str - text of frame label
        alist:list - items in pulldown
        orient:str - 'horizontal' or 'vertical'
        gap:int - space between widget frames
        -> [ttk.Radiobuttons] """
        self.result[rowcol] = ['radio', tk.StringVar()] # init var to tk var
        frame = ttk.LabelFrame(self, text=prompt)
        rbuttons = []                                  # list for radiobuttons
        for n, item in enumerate(alist):               # for every item in the given list
            radiobutton = ttk.Radiobutton(frame, width=width, text=item,
                variable=self.result[rowcol][1], value=item) # create the radiobutton
            if orient == 'vertical':
                radiobutton.grid(row=n, column=0)      # grid it
            else:
                radiobutton.grid(row=0, column=n)
            rbuttons.append(radiobutton)
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return rbuttons                                # list of radiobuttons

    def makeOption(self, rowcol, prompt, alist, gap=3):
        """ create a option list
        rowcol:int - row or column number
        prompt:str - text of frame label
        alist:list - items in pulldown
        gap:int - space between widget frames
        -> tk.OptionMenu """
        self.result[rowcol] = ['option', tk.StringVar()] # init var to tk var
        frame = ttk.LabelFrame(self, text=prompt)
        option = tk.OptionMenu(frame, self.result[rowcol][1], *alist) # create optionmenu
        option.grid(sticky='w')
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return option                                  # optionmenu

    def makeOpen(self, rowcol, width, prompt, gap=3, **parms):
        """ create a open file entry with a browse button
        rowcol:int - row or column number
        width:int - width of entry widget
        prompt:str - text of frame label
        gap:int - space between widget frames
        parms:dictionary - labeled arguments to askopenfilename
        -> ttk.Entry """
        self.result[rowcol] = ['open', tk.StringVar()] # init var to tk var
        frame = ttk.LabelFrame(self, text=prompt)
        entry = ttk.Entry(frame, textvariable=self.result[rowcol][1], width=width) # create entry
        entry.grid(padx=3, pady=3)                     # grid entry in frame
        command = (lambda: self._openDialog(rowcol, **parms))
        #photo = tk.PhotoImage(file='openfolder.gif')  # optional folder icon
        #button = ttk.Button(frame, image=photo, command=command)
        button = ttk.Button(frame, width=7, text='Browse', command=command) # create button
        button.grid(row=0, column=1, padx=3)           # grid button in frame
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return [entry, button]                         # list of entry and button

    def _openDialog(self, rowcol, **parms):
        """ create the file browsing window
        rowcol:int - row or column number
        parms:dictionary - labeled arguments to askopenfilename """
        fn = askopenfilename(**parms)                  # create the file dialog
        if fn:                                         # user selected file?
            self.setParameter(rowcol, fn)              # store it in result

    def makeSaveAs(self, rowcol, width, prompt, gap=3, **parms):
        """ create a open file entry with a browse button
        rowcol:int - row or column number
        width:int - width of entry widget
        prompt:str - text of frame label
        gap:int - space between widget frames
        parms:dictionary - labeled arguments to asksaveasfilename
        -> [ttk.Entry, ttk.Button] """
        self.result[rowcol] = ['saveas', tk.StringVar()] # very similar to makeInput
        frame = ttk.LabelFrame(self, text=prompt)
        entry = ttk.Entry(frame, textvariable=self.result[rowcol][1], width=width)
        entry.grid(padx=3, pady=3)
        button = ttk.Button(frame, width=7, text='Browse',
            command=(lambda: self._saveDialog(rowcol, **parms)))
        button.grid(row=0, column=1, padx=3, pady=3)
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return [entry, button]                         # list of entry and button

    def _saveDialog(self, rowcol, **parms):
        """ create the file browsing window
        rowcol:int - row or column number
        parms:dictionary - labeled arguments to askopenfilename """
        fn = asksaveasfilename(**parms)                # similar to _openDialog
        if fn:
            self.setParameter(rowcol, fn)

    def makeTreeList(self, rowcol, height, prompt, columns, rows, gap=3):
        """ create a treeview that displays only lists
        rowcol:int - row or column number
        height:int - height of widget
        prompt:str - text of frame label
        columns:list - the column headers and width
        rows:list - list of widget row results to add to list
        gap:int - space between widget frames
        -> [ttk.Treeview, ttk.Button, ttk.Button] """
        # we must create a parallel storage for the data because the data must
        # exist after the window and widget are destroyed
        frame = ttk.LabelFrame(self, text=prompt)
        titles = [item[0] for item in columns]         # create the column titles
        tree = ttk.Treeview(frame, columns=titles, show='headings',
            selectmode='browse', height=height)        # create treeview
        self.result[rowcol] = ['tree', [[], tree]]     # must keep the data and tree
        xscroll = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
        yscroll = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        for title, width in columns:                   # init column headers
            tree.heading(title, text=title, anchor='w') # set the title
            tree.column(title, width=width, stretch=False) # set the width
        tree.grid(row=0, column=0, pady=3)             # grid the tree
        xscroll.grid(row=1, column=0, sticky='we')
        yscroll.grid(row=0, column=1, sticky='ns')
        buttonFrame = ttk.Frame(frame)                 # create the add/delete frame
        buttonFrame.grid(row=0, column=2, padx=3)      # grid the frame
        addbutton = ttk.Button(buttonFrame, width=6, text='Add',
            command=(lambda: self._addrow(rowcol, rows))) # create add button
        subbutton = ttk.Button(buttonFrame, width=6, text='Delete',
            command=(lambda: self._delrow(rowcol)))    # create delete button
        addbutton.grid(row=0, padx=1, pady=3)          # grid buttons
        subbutton.grid(row=1, padx=1, pady=3)
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return [tree, addbutton, subbutton]            # list of treeview and buttons

    def _addrow(self, treerow, rows):
        """ add items from other widgets to the treeview
        treerow:int - the treeview row
        rows:list - the row numbers of the other widgets """
        contents, tree = self.result[treerow][1]       # get the widget, and contents
        items = []                                     # create items list
        for i in rows:                                 # check each widget
            value = self.getParameter(i)
            items.append(value)                   # get the contents of other widgets
            if self.result[i][0] not in ['spin', 'option']:
                self.setParameter(i, '')               # clear the widget
        for item in items:
            if item:
                break
        else:                                          # no breaks so...
            return                                     # don't add empty lists
        self.setParameter(treerow, items)

    def _delrow(self, treerow):
        """ delete selected row from treeview
        treerow:int - the treeview row """
        contents, tree = self.result[treerow][1]
        select = tree.selection()                      # get the selection
        if select:
            index = tree.index(select)
            del contents[index]
            tree.delete(select)                        # remove from treeview

    def makeScale(self, rowcol, length, width, prompt, parms, gap=3, orient='horizontal'):
        """ create a integer scale with entry box
        rowcol:int - row or column number
        length:int - length of scale
        width:int - width of entry widget
        prompt:str - text of frame label
        parms:list - parms of scale [from, to, initial]
        gap:int - space between widget frames
        -> ttk.Scale """
        self.result[rowcol] = ['scale', tk.IntVar()]
        from_, to, init = parms
        frame = ttk.LabelFrame(self, text=prompt)      # create frame
        scale = ttk.Scale(frame, length=length, from_=from_, to=to, value=init,
            variable=self.result[rowcol][1], orient=orient,
            command=lambda x: self.setParameter(rowcol, int(float(x)))) # create scale
        # the lambda causes the values to always be integers
        current = ttk.Entry(frame, width=width, textvariable=self.result[rowcol][1]) # create entry
        self.setParameter(rowcol, init)                # initialize scale
        scale.grid(row=0, column=0)
        current.grid(row=0, column=1, padx=3)
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return [scale, current]                        # list of scale and entry

    def makeSpin(self, rowcol, width, prompt, parms, between='', gap=3):
        """ create a group of spinboxes
        rowcol:int - row or column number
        width:int - width of spinboxes
        prompt:str - text of frame label
        parms:list - the parmeters for each spinbox [from, to, initial]
        between: str - the label between each box
        gap:int - space between widget frames
        -> [ttk.Spinboxes] """
        self.result[rowcol] = ['spin', [[], between]]  # data is list
        frame = ttk.LabelFrame(self, text=prompt)
        col = 0                                        # set col
        spins = []
        for parm in parms:
            from_, to, init = parm                     # extract spinbox parms
            self.result[rowcol][1][0].append(tk.IntVar()) # add tkvar to list
            spin = tk.Spinbox(frame, width=width, from_=from_, to=to,
                textvariable=self.result[rowcol][1][0][col/2]) # make spinbox
            self.result[rowcol][1][0][col/2].set(init) # init it
            spin.grid(row=0, column=col)               # grid it
            spins.append(spin)                         # add it to list
            col += 1                                   # next column
            label = ttk.Label(frame, text=between)     # add the between str
            label.grid(row=0, column=col)              # grid the it
            col += 1
        label.destroy()                                # remove last between str
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return spins                                   # list of spinboxes

    def makeText(self, rowcol, width, height, prompt, gap=3):
        """ create a text window
        rowcol:int - row or column number
        width:int - width of window (chars)
        height:int - height of window (chars)
        prompt:int - label of frame
        gap:int - space between widget frames
        -> tk.text """
        frame = ttk.LabelFrame(self, text=prompt)
        text = tk.Text(frame, width=width, height=height) # make text widget
        self.result[rowcol] = ['text', text]
        text.grid(row=0, sticky='wens')                # fill entire frame
        vbar = ttk.Scrollbar(frame)                    # make scrollbar
        text['yscrollcommand'] = vbar.set              # connect text to scrollbar
        text['font'] = ('Helvetica', '10')             # default font
        vbar['command'] = text.yview                   # connect scrollbar to text
        vbar.grid(row=0, column=1, sticky='ns')        # grid scrollbar
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return text

    def makeButtons(self, rowcol, cmd=[], space=3, gap=3, orient='horizontal'):
        """ create a button bar, defaults to Ok - Cancel
        rowcol:int - row or column number
        cmd:list - [label:str, callback:function] for each button
        space:int - space between buttons
        gap:int - space between widgets frames
        orient:str - orient of button bar
        -> [ttk.Buttons] """
        if not cmd:                                    # use default buttons
            cmd = [['Ok',self._collect],['Cancel',self._cancel]]
        frame = ttk.Frame(self)
        buttons = []                                   # list for created buttons
        n = 0
        for label, callback in cmd:
            button = ttk.Button(frame, width=12, text=label,
              command=callback)                        # create button
            if orient == 'horizontal':
                button.grid(row=0, column=n, padx=space) # grid it
                n += 1
            else:                                      # 'vertical'
                button.grid(row=n, column=0, pady=space) # grid it
                n += 1
            buttons.append(button)                     # add to list
        if self.worient == 'vertical':
            frame.grid(row=rowcol, column=0, pady=gap) # grid titled frame
        else:
            frame.grid(row=0, column=rowcol, padx=gap)
        return buttons                                 # list of created buttons

    def _collect(self):
        """ close the dialog, data is stored in self.result """
        self.close()                                   # close the dialog window...
                                                       # but keep result
    def _cancel(self):
        """ close the dialog, self.result is cleared """
        self.result = None                             # clear result
        self.close()                                   # close the dialog window

    # the following widgets are containers to other widgets

    def makeNotebook(self, row, tabs):
        """ create a tabbed notebook
        tabs:[str] - titles of each tab page
        -> [notebook, [pages]] """
        self.result[row] = ['notebook', [tabs]]        # data is list of lists
        pages = []                                     # pages will be other frames
        notebook = ttk.Notebook(self)                  # create notebook
        for page in tabs:                              # each tab is a page
            frame = ttk.Frame(self)                    # create frame
            notebook.add(frame, text=page, sticky='wens') # fill up the entire page
            pages.append(frame)                        # remember created frames
        self.result[row][1].append(notebook)           # add widget
        return [notebook, pages]                       # must manually grid

    def makeFrame(self, prompt):
        """ create a labeled lrame
        prompt:str - frame label """
        frame = ttk.LabelFrame(self, text=prompt)
        return frame                                   # must manually grid

    # support functions

    def getParameter(self, row):
        """ get the contents of the widget, same as value = dialog[row]
        row:int - the row number
        -> object """
        if self.result[row]:
            widgetType, widget = self.result[row]      # get type and widget
            if widgetType in ('label','entry','combo','radio','open','saveas',
                'option','scale'):
                value = widget.get()
            elif widgetType == 'checks':               # data type is dict
                value = []                             # create list
                for key in widget:                     # for every key...
                    if widget[key].get():              # check boolean value
                        value.append(key)              # add key to list
            elif widgetType == 'tree':
                contents, tree = widget
                value = contents                       # get the list
            elif widgetType == 'spin':
                ints, sep = widget
                value = []
                for item in ints:
                    value.append(item.get())           # get the tk var
            elif widgetType == 'notebook':
                headers, notebook = widget
                page = notebook.index('current')       # get current page
                value = headers[page]                  # lookup page header
            return value

    def setParameter(self, row, value):
        """ set the contents of the widget, same as dialog[row] = value
        row:init - row number
        value:object - value to set """
        widgetType, widget = self.result[row]          # get type and widget
        if widgetType in ('label','entry','combo','radio','open','saveas',
            'option','scale'):
            widget.set(value)
        elif widgetType == 'checks':
            for key in widget:                         # for every key in list...
                widget[key].set(key in value)          # set tk boolean
        elif widgetType == 'tree':
            contents, tree = widget                    # split temp
            if value is not None:                      # non-empty list
                tree.insert('', 'end', values=value)   # add to tree
                contents.append(value)
            else:                                      # empty list, delete tree branches
                for iid in tree.get_children():
                    tree.delete(iid)                   # delete branch
                self.result[row][1][0] = []            # clear contents
        elif widgetType == 'spin':
            for item in widget[0]:                     # for spinboxes
                if value == '':
                    item.set('')                       # clear it
                else:
                    item.set(value.pop(0))             # set it and get next
        elif widgetType == 'notebook':
            headers, notebook = widget
            page = headers.index(value)                # get page header index
            notebook.select(page)                      # display that page
        elif widgetType == 'text':
            if value is not None:
               widget.insert('end', value)             # add message
               widget.see('end')                       # scroll text so it is visible
            else:
               widget.delete('1.0', 'end')             # clear everything
            widget.update()                            # update display

    def waitforUser(self):
        """ alias for mainloop, better label for beginners """
        self.mainloop()

    def close(self):
        """ close the dialog """
        self.master.destroy()

    def catchExcept(self):
        """ catch the exception messages
        -> str: exception messge """
        import traceback
        msg = traceback.format_exc()
        return msg

class EzMessage(tk.Frame):
    """ easy message window creator """

    def __init__(self, master=None, wait=True, width=60, height=20):
        """ create an output window
        master:tk.toplevel - container widget
        wait:bool - create a button which lets user close window
        width:int - width of window, chars
        height:int - height of window, chars """
        tk.Frame.__init__(self, master)                # create frame
        self._buildWidgets(wait, width, height)        # build the widgets

    def _buildWidgets(self, wait, width, height):
        """ build the widget
        wait:bool - create a button which lets user close window
        width:int - width of window, chars
        height:int - height of window, chars """
        self.text = tk.Text(self, width=width, height=height) # make text widget
        self.text.grid(row=0, sticky='wens')           # fill entire frame
        vbar = ttk.Scrollbar(self)                     # make scrollbars
        self.text['yscrollcommand'] = vbar.set         # connect text to scrollbars
        self.text['font'] = ('Helvetica', '10')        # set font
        vbar['command'] = self.text.yview              # connect scrollbar to text
        vbar.grid(row=0, column=1, sticky='ns')
        if wait:                                       # need acknowledge button?
            self.button = ttk.Button(self, text='Ok',  # create acknowledge button
                width=8, command=self.close)
            self.button.grid(row=2, column=0)
        self.text.rowconfigure(0, weight=1)            # make the text widget resizable
        self.text.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)                 # make the frame resizable
        self.columnconfigure(0, weight=1)
        top = self.winfo_toplevel()                    # make the window resizable
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

    def setTitle(self, prompt):
        """ set the title for a window
        prompt:str - the title """
        self.master.title(prompt)

    def addMessage(self, message, delay=0):
        """ print a message in the output window
        message:str - message
        delay:int - secs to delay """
        self.text.insert('end', message)               # add message
        self.text.see('end')                           # scroll text so it is visible
        self.text.update()                             # update display
        time.sleep(delay)                              # pause delay seconds

    def clear(self):
        """ clear the output window """
        self.text.delete('1.0', 'end')                 # clear everything
        self.text.update()                             # update display

    def close(self):
        self.master.destroy()

    def catchExcept(self, wait=True):
        """ send all error messages to message window """
        import traceback
        msg = traceback.format_exc()
        self.addMessage('\n'+msg+'\n')                 # add error message
        if wait:
            self.mainloop()

    def waitforUser(self):
        """ alias for mainloop, better label for beginners """
        self.mainloop()

