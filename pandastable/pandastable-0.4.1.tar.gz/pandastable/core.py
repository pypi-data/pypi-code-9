#!/usr/bin/env python
"""
    Implements the core pandastable classes.
    Created Jan 2014
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox, simpledialog
import tkinter.font
import math, time
import os, types
import string, copy
import platform
import numpy as np
import pandas as pd
from .data import TableModel
from .headers import ColumnHeader, RowHeader
from .plotting import MPLBaseOptions, PlotViewer
from .prefs import Preferences
from .dialogs import ImportDialog
from . import images
from .dialogs import *

class Table(Canvas):
    """A tkinter class for providing table functionality"""

    def __init__(self, parent=None, model=None, dataframe=None,
                   width=None, height=None,
                   rows=50, cols=10, showtoolbar=False, showstatusbar=False,
                   **kwargs):
        Canvas.__init__(self, parent, bg='white',
                         width=width, height=height,
                         relief=GROOVE,
                         scrollregion=(0,0,300,200))
        self.parentframe = parent
        #get platform into a variable
        self.ostyp = self.checkOS()
        self.platform = platform.system()
        self.width = width
        self.height = height
        self.filename = None
        self.showtoolbar = showtoolbar
        self.showstatusbar = showstatusbar
        self.set_defaults()

        self.currentpage = None
        self.navFrame = None
        self.currentrow = 0
        self.currentcol = 0
        self.reverseorder = 0
        self.startrow = self.endrow = None
        self.startcol = self.endcol = None
        self.allrows = False
        self.multiplerowlist=[]
        self.multiplecollist=[]
        self.col_positions=[]
        self.mode = 'normal'
        self.editable = True
        self.filtered = False
        self.child = None
        self.queryrow = 4
        self.childrow = 5
        self.loadPrefs()
        self.currentdir = os.path.expanduser('~')
        #set any options passed in kwargs to overwrite defaults and prefs
        for key in kwargs:
            self.__dict__[key] = kwargs[key]

        if dataframe is not None:
            self.model = TableModel(dataframe=dataframe)
        elif model != None:
            self.model = model
        else:
            self.model = TableModel(rows=rows,columns=cols)

        self.rows = self.model.getRowCount()
        self.cols = self.model.getColumnCount()
        self.tablewidth = (self.cellwidth)*self.cols
        self.doBindings()

        #column specific actions, define for every column type in the model
        #when you add a column type you should edit this dict
        self.columnactions = {'text' : {"Edit":  'drawCellEntry' },
                              'number' : {"Edit": 'drawCellEntry' }}
        self.setFontSize()
        return

    def set_defaults(self):
        """Set default settings"""

        self.cellwidth=100
        self.maxcellwidth=300
        self.rowheight=20
        self.horizlines=1
        self.vertlines=1
        self.alternaterows=0
        self.autoresizecols = 0
        self.inset=2
        self.x_start=0
        self.y_start=1
        self.linewidth=1.0
        self.rowheaderwidth=40
        self.showkeynamesinheader=False
        self.thefont = ('Arial',12)
        self.cellbackgr = '#F7F7FA'
        self.entrybackgr = 'white'
        self.grid_color = '#ABB1AD'
        #self.selectedcolor = '#F3F781'
        self.rowselectedcolor = '#CCCCFF'
        self.multipleselectioncolor = '#E0F2F7'
        self.boxoutlinecolor = '#084B8A'
        return

    def setFontSize(self):
        """Set font size to match font, we need to get rid of fontsize as
            a separate variable?"""

        if hasattr(self, 'thefont') and type(self.thefont) is tuple:
            self.fontsize = self.thefont[1]
        return

    def mouse_wheel(self, event):
        """Handle mouse wheel scroll for windows"""

        if event.num == 5 or event.delta == -120:
            event.widget.yview_scroll(1, UNITS)
            self.tablerowheader.yview_scroll(1, UNITS)
        if event.num == 4 or event.delta == 120:
            if self.canvasy(0) < 0:
                return
            event.widget.yview_scroll(-1, UNITS)
            self.tablerowheader.yview_scroll(-1, UNITS)
        self.redrawVisible()
        return

    def doBindings(self):
        """Bind keys and mouse clicks, this can be overriden"""

        self.bind("<Button-1>",self.handle_left_click)
        self.bind("<Double-Button-1>",self.handle_double_click)
        self.bind("<Control-Button-1>", self.handle_left_ctrl_click)
        self.bind("<Shift-Button-1>", self.handle_left_shift_click)

        self.bind("<ButtonRelease-1>", self.handle_left_release)
        if self.ostyp=='mac':
            #For mac we bind Shift, left-click to right click
            self.bind("<Button-2>", self.handle_right_click)
            self.bind('<Shift-Button-1>',self.handle_right_click)
        else:
            self.bind("<Button-3>", self.handle_right_click)

        self.bind('<B1-Motion>', self.handle_mouse_drag)
        self.bind('<Motion>', self.handle_motion)

        self.bind("<Control-c>", self.copy)
        #self.bind("<Control-x>", self.deleteRow)
        #self.bind_all("<Control-n>", self.addRow)
        self.bind("<Delete>", self.clearData)
        self.bind("<Control-v>", self.paste)
        self.bind("<Control-a>", self.selectAll)

        self.bind("<Right>", self.handle_arrow_keys)
        self.bind("<Left>", self.handle_arrow_keys)
        self.bind("<Up>", self.handle_arrow_keys)
        self.bind("<Down>", self.handle_arrow_keys)
        self.parentframe.master.bind_all("<KP_8>", self.handle_arrow_keys)
        self.parentframe.master.bind_all("<Return>", self.handle_arrow_keys)
        self.parentframe.master.bind_all("<Tab>", self.handle_arrow_keys)
        #if 'windows' in self.platform:
        self.bind("<MouseWheel>", self.mouse_wheel)
        self.bind('<Button-4>', self.mouse_wheel)
        self.bind('<Button-5>', self.mouse_wheel)
        self.focus_set()
        return

    def show(self, callback=None):
        """Adds column header and scrollbars and combines them with
           the current table adding all to the master frame provided in constructor.
           Table is then redrawn."""

        #Add the table and header to the frame
        self.tablerowheader = RowHeader(self.parentframe, self, width=self.rowheaderwidth)
        self.tablecolheader = ColumnHeader(self.parentframe, self)
        self.Yscrollbar = AutoScrollbar(self.parentframe,orient=VERTICAL,command=self.set_yviews)
        self.Yscrollbar.grid(row=1,column=2,rowspan=1,sticky='news',pady=0,ipady=0)
        self.Xscrollbar = AutoScrollbar(self.parentframe,orient=HORIZONTAL,command=self.set_xviews)
        self.Xscrollbar.grid(row=2,column=1,columnspan=1,sticky='news')
        self['xscrollcommand'] = self.Xscrollbar.set
        self['yscrollcommand'] = self.Yscrollbar.set
        self.tablecolheader['xscrollcommand'] = self.Xscrollbar.set
        self.tablerowheader['yscrollcommand'] = self.Yscrollbar.set
        self.parentframe.rowconfigure(1,weight=1)
        self.parentframe.columnconfigure(1,weight=1)

        self.tablecolheader.grid(row=0,column=1,rowspan=1,sticky='news')
        self.tablerowheader.grid(row=1,column=0,rowspan=1,sticky='news')
        self.grid(row=1,column=1,rowspan=1,sticky='news',pady=0,ipady=0)

        self.adjustColumnWidths()
        self.parentframe.bind("<Configure>", self.redrawVisible)
        self.tablecolheader.xview("moveto", 0)
        self.xview("moveto", 0)
        if self.showtoolbar == True:
            self.toolbar = ToolBar(self.parentframe, self)
            self.toolbar.grid(row=0,column=3,rowspan=2,sticky='news')
        if self.showstatusbar == True:
            self.statusbar = statusBar(self.parentframe, self)
            self.statusbar.grid(row=3,column=0,columnspan=2,sticky='ew')
        self.redraw(callback=callback)
        return

    def remove(self):
        """Close table frame"""
        self.parentframe.destroy()
        return

    def getVisibleRegion(self):
        """Get visible region of canvas"""
        x1, y1 = self.canvasx(0), self.canvasy(0)
        #w, h = self.winfo_width(), self.winfo_height()
        #if w <= 1.0 or h <= 1.0:
        w, h = self.master.winfo_width(), self.master.winfo_height()
        x2, y2 = self.canvasx(w), self.canvasy(h)
        return x1, y1, x2, y2

    def getRowPosition(self, y):
        """Set row position"""
        h = self.rowheight
        y_start = self.y_start
        row = (int(y)-y_start)/h
        if row < 0:
            return 0
        if row > self.rows:
            row = self.rows
        return int(row)

    def getColPosition(self, x):
        x_start = self.x_start
        w = self.cellwidth
        i=0
        col=0
        for c in self.col_positions:
            col = i
            if c+w>=x:
                break
            i+=1
        return int(col)

    def getVisibleRows(self, y1, y2):
        """Get the visible row range"""
        start = self.getRowPosition(y1)
        end = self.getRowPosition(y2)+1
        if end > self.rows:
            end = self.rows
        return start, end

    def getVisibleCols(self, x1, x2):
        """Get the visible column range"""
        start = self.getColPosition(x1)
        end = self.getColPosition(x2)+1
        if end > self.cols:
            end = self.cols
        return start, end

    def redrawVisible(self, event=None, callback=None):
        """Redraw the visible portion of the canvas"""

        model = self.model
        self.rows = len(self.model.df.index)
        self.cols = len(self.model.df.columns)
        if self.cols == 0 or self.rows == 0:
            self.delete('entry')
            self.delete('rowrect')
            self.delete('currentrect')
            self.delete('gridline','text')
            return
        self.tablewidth = (self.cellwidth) * self.cols
        self.configure(bg=self.cellbackgr)
        self.setColPositions()

        #are we drawing a filtered subset of the recs?
        if self.filtered == True:
            self.delete('colrect')

        self.rowrange = list(range(0,self.rows))
        self.configure(scrollregion=(0,0, self.tablewidth+self.x_start,
                self.rowheight*self.rows+10))

        x1, y1, x2, y2 = self.getVisibleRegion()
        startvisiblerow, endvisiblerow = self.getVisibleRows(y1, y2)
        self.visiblerows = list(range(startvisiblerow, endvisiblerow))
        startvisiblecol, endvisiblecol = self.getVisibleCols(x1, x2)
        self.visiblecols = list(range(startvisiblecol, endvisiblecol))

        self.drawGrid(startvisiblerow, endvisiblerow)
        align = self.align
        self.delete('fillrect')
        bgcolor = self.cellbackgr
        df = self.model.df
        for row in self.visiblerows:
            cols = df.iloc[row,:].fillna('')
            for col in self.visiblecols:
                text = cols[col]
                self.drawText(row, col, text, align)

        self.tablecolheader.redraw()
        self.tablerowheader.redraw(align=self.align)
        self.drawSelectedRow()
        self.drawSelectedRect(self.currentrow, self.currentcol)
        if len(self.multiplerowlist)>1:
            self.tablerowheader.drawSelectedRows(self.multiplerowlist)
            self.drawMultipleRows(self.multiplerowlist)
            self.drawMultipleCells()
        return

    def redraw(self, event=None, callback=None):
        self.redrawVisible(event, callback)
        if hasattr(self, 'statusbar'):
            self.statusbar.update()
        return

    def redrawCell(self, row=None, col=None, recname=None, colname=None):
        """Redraw a specific cell only"""

        text = self.model.getValueAt(row,col)
        self.delete('celltext'+str(col)+'_'+str(row))
        self.drawText(row, col, text)
        return

    def getScale(self):
        try:
            fontsize = self.thefont[1]
        except:
            fontsize = self.fontsize
        scale = 8.5 * float(fontsize)/9
        return scale

    def adjustColumnWidths(self):
        """Optimally adjust col widths to accomodate the longest entry
            in each column - usually only called  on first redraw"""

        #obj = self.find_withtag(ALL)
        #print (obj)
        #x1, y1, x2, y2 = self.bbox(obj)
        #self.find_overlapping(x1, y1, x2, y2)
        try:
            fontsize = self.thefont[1]
        except:
            fontsize = self.fontsize
        scale = self.getScale()
        for col in range(self.cols):
            colname = self.model.getColumnName(col)
            if colname in self.model.columnwidths:
                w = self.model.columnwidths[colname]
            else:
                w = self.cellwidth
            l = self.model.getlongestEntry(col)
            size = l * scale
            if size < w:
                continue
            #print (col, l,size, self.cellwidth)
            if size >= self.maxcellwidth:
                size = self.maxcellwidth
            self.model.columnwidths[colname] = size + float(fontsize)/12*6
        return

    def autoResizeColumns(self):
        """Automatically set nice column widths and draw"""

        self.adjustColumnWidths()
        self.redraw()
        return

    def setColPositions(self):
        """Determine current column grid positions"""

        df = self.model.df
        self.col_positions=[]
        w = self.cellwidth
        x_pos = self.x_start
        self.col_positions.append(x_pos)
        for col in range(self.cols):
            #colname = self.model.getColumnName(col)
            colname = df.columns[col]
            if colname in self.model.columnwidths:
                x_pos=x_pos+self.model.columnwidths[colname]
            else:
                x_pos=x_pos+w
            self.col_positions.append(x_pos)
        self.tablewidth = self.col_positions[len(self.col_positions)-1]
        return

    def sortTable(self, columnIndex=None, ascending=1, index=False):
        """Set up sort order dict based on currently selected field"""

        if columnIndex==None:
            columnIndex = self.multiplecollist
        df = self.model.df
        if index == True:
            df.sort_index(inplace=True)
        else:
            colnames = list(df.columns[columnIndex])
            df.sort(colnames, inplace=True, ascending=ascending)
        self.redraw()
        return

    def groupby(self, colindex):
        grps = self.model.groupby(colindex)
        for i,g in grps:
            print(g)
        return

    def setindex(self):
        """Set indexes"""
        cols = self.multiplecollist
        self.model.setindex(cols)
        self.setSelectedCol(0)
        self.redraw()
        self.drawSelectedCol()
        if hasattr(self, 'pf'):
            self.pf.updateData()
        return

    def resetIndex(self):
        """Reset index and redraw row header"""
        self.model.resetIndex()
        self.redraw()
        self.drawSelectedCol()
        if hasattr(self, 'pf'):
            self.pf.updateData()
        return

    def copyIndex(self):
        """Copy index to a column"""
        self.model.copyIndex()
        self.redraw()
        return

    def showIndex(self):
        self.tablerowheader.showindex = True
        return

    def set_xviews(self,*args):
        """Set the xview of table and col header"""

        self.xview(*args)
        self.tablecolheader.xview(*args)
        self.redrawVisible()
        return

    def set_yviews(self,*args):
        """Set the xview of table and row header"""

        self.yview(*args)
        self.tablerowheader.yview(*args)
        self.redrawVisible()
        return

    def addRow(self):
        """Insert a new row"""

        row = self.getSelectedRow()
        key = self.model.addRow(row)
        self.redraw()
        return

    def addRows(self, num=None):
        """Add new rows"""

        if num == None:
            num = simpledialog.askinteger("Now many rows?",
                                            "Number of rows:",initialvalue=1,
                                             parent=self.parentframe)
        if not num:
            return
        keys = self.model.autoAddRows(num)
        self.redraw()
        return

    def addColumn(self, newname=None):
        """Add a new column"""

        if newname == None:
            coltypes = ['object','float64']
            d = MultipleValDialog(title='New Column',
                                    initialvalues=(coltypes, ''),
                                    labels=('Column Type','Name'),
                                    types=('combobox','string'),
                                    parent = self.parentframe)
            if d.result == None:
                return
            else:
                dtype = d.results[0]
                newname = d.results[1]

        if newname != None:
            if newname in self.model.df.columns:
                messagebox.showwarning("Name exists",
                                        "Name already exists!",
                                        parent=self.parentframe)
            else:
                self.model.addColumn(newname, dtype)
                self.parentframe.configure(width=self.width)
                self.redraw()
        return

    def deleteRow(self):
        """Delete a row"""

        if len(self.multiplerowlist)>1:
            n = messagebox.askyesno("Delete",
                                      "Delete selected rows?",
                                      parent=self.parentframe)
            if n == True:
                rows = self.multiplerowlist
                self.model.deleteRows(rows)
                self.setSelectedRow(0)
                self.clearSelected()
                self.redraw()
        else:
            n = messagebox.askyesno("Delete",
                                      "Delete this row?",
                                      parent=self.parentframe)
            if n:
                row = self.getSelectedRow()
                self.model.deleteRow(row)
                self.setSelectedRow(row-1)
                self.clearSelected()
                self.redraw()
        return

    def deleteColumn(self):
        """Delete currently selected column(s)"""
        n =  messagebox.askyesno("Delete",
                                   "Delete Column(s)?",
                                   parent=self.parentframe)
        if n:
            cols = self.multiplecollist
            self.model.deleteColumns(cols)
            self.setSelectedCol(0)
            self.redraw()
            self.drawSelectedCol()
            if hasattr(self, 'pf'):
                self.pf.updateData()
        return

    def deleteCells(self, rows, cols):
        """Clear the cell contents"""

        n =  messagebox.askyesno("Clear Confirm",
                                   "Clear this data?",
                                   parent=self.parentframe)
        if not n:
            return
        self.model.deleteCells(rows, cols)
        self.redraw()
        return

    def clearData(self, evt=None):
        """Delete cells from gui event"""
        rows = self.multiplerowlist
        cols = self.multiplecollist
        self.deleteCells(rows, cols)
        return

    def clearTable(self):
        """Make an empty table"""
        n =  messagebox.askyesno("Clear Confirm",
                                   "This will clear the entire table.\nAre you sure?",
                                   parent=self.parentframe)
        if not n:
            return
        model = TableModel(pd.DataFrame())
        self.updateModel(model)
        self.redraw()
        return

    def autoAddColumns(self, numcols=None):
        """Automatically add x number of cols"""
        if numcols == None:
            numcols = simpledialog.askinteger("Auto add rows.",
                                                "How many empty columns?",
                                                parent=self.parentframe)
        self.model.auto_AddColumns(numcols)
        self.parentframe.configure(width=self.width)
        self.redraw()
        return

    def setColumnType(self):
        """Change the column dtype"""

        df = self.model.df
        col = df.columns[self.currentcol]
        coltypes = ['object','str','int','float64','datetime64[ns]']
        curr = df[col].dtype
        d = MultipleValDialog(title='current type is %s' %curr,
                                initialvalues=[coltypes],
                                labels=['Type:'],
                                types=['combobox'],
                                parent = self.parentframe)
        if d.result == None:
            return
        t = d.results[0]
        try:
            self.model.df[col] = df[col].astype(t)
            self.redraw()
        except:
            print('failed')
        return

    def findValue(self, searchstring=None, findagain=None):
        """Return the row/col for the input value"""
        if searchstring == None:
            searchstring = simpledialog.askstring("Search table.",
                                               "Enter search value",
                                               parent=self.parentframe)
        found=0
        if findagain == None or not hasattr(self,'foundlist'):
            self.foundlist=[]
        if self.model!=None:
            for row in range(self.rows):
                for col in range(self.cols):
                    text = str(self.model.getValueAt(row,col))
                    if text=='' or text==None:
                        continue
                    cell=row,col
                    if findagain == 1 and cell in self.foundlist:
                        continue
                    if text.lower().find(searchstring.lower())!=-1:
                        print('found in',row,col)
                        found=1
                        #highlight cell
                        self.delete('searchrect')
                        self.drawRect(row, col, color='red', tag='searchrect', delete=0)
                        self.lift('searchrect')
                        self.lift('celltext'+str(col)+'_'+str(row))
                        #add row/col to foundlist
                        self.foundlist.append(cell)
                        #need to scroll to centre the cell here..
                        x,y = self.getCanvasPos(row, col)
                        self.xview('moveto', x)
                        self.yview('moveto', y)
                        self.tablecolheader.xview('moveto', x)
                        self.tablerowheader.yview('moveto', y)
                        return row, col
        if found==0:
            self.delete('searchrect')
            print('nothing found')
            return None

    def showAll(self):
        """Re-show unfiltered"""
        if hasattr(self, 'dataframe'):
            self.model.df = self.dataframe
        self.filtered = False
        self.redraw()
        return

    def query(self, evt=None):
        """Do query"""
        s = self.queryvar.get()
        if s=='':
            self.showAll()
            return
        if self.filtered == True:
            self.model.df = self.dataframe
        df = self.model.df
        filtdf = df.query(s)
        #replace current dataframe but keep a copy!
        self.dataframe = self.model.df.copy()
        self.model.df = filtdf
        self.filtered = True
        self.redraw()
        return

    def queryBar(self, evt=None):
        """Use string query to filter. Will not work with spaces in column
        names, so these would need to be converted first."""

        def reset():
            self.qframe.destroy()
            self.qframe = None
            self.showAll()
        if hasattr(self, 'qframe') and self.qframe != None:
            return
        qf = self.qframe = Frame(self.parentframe)
        self.qframe.grid(row=self.queryrow,column=1,sticky='news')
        self.queryvar = StringVar()
        e = Entry(qf, textvariable=self.queryvar, font="Courier 12 bold")#, validatecommand=self.query)
        e.bind('<Return>', self.query)
        e.pack(fill=BOTH,side=LEFT,expand=1,padx=2,pady=2)
        b = Button(qf,text='find',width=5,command=self.query)
        b.pack(fill=BOTH,side=LEFT,padx=2,pady=2)
        b = Button(qf,text='close',width=5,command=reset)
        b.pack(fill=BOTH,side=LEFT,padx=2,pady=2)
        return

    def applyFunction(self, evt=None):
        """Apply a string based function to create new columns"""

        self.convertNumeric()
        s = self.evalvar.get()
        if s=='':
            return
        df = self.model.df
        e = df.eval(s)
        if type(e) is pd.DataFrame:
            self.model.df = e
        self.redraw()
        if hasattr(self, 'pf'):
            self.plotSelected()
        #keep a copy?
        #self.dataframe = self.model.df.copy()
        return

    def evalBar(self, evt=None):
        """Use pd.eval to apply a function."""

        def reset():
            self.evalframe.destroy()
            self.evalframe = None
            self.showAll()
        if hasattr(self, 'evalframe') and self.evalframe != None:
            return
        ef = self.evalframe = Frame(self.parentframe)
        ef.grid(row=self.queryrow,column=1,sticky='news')
        self.evalvar = StringVar()
        e = Entry(ef, textvariable=self.evalvar, font="Courier 13 bold")
        e.bind('<Return>', self.applyFunction)
        e.pack(fill=BOTH,side=LEFT,expand=1,padx=2,pady=2)
        b = Button(ef,text='apply',width=5,command=self.applyFunction)
        b.pack(fill=BOTH,side=LEFT,padx=2,pady=2)
        b = Button(ef,text='close',width=5,command=reset)
        b.pack(fill=BOTH,side=LEFT,padx=2,pady=2)
        return

    def resizeColumn(self, col, width):
        """Resize a column by dragging"""

        colname = self.model.getColumnName(col)
        self.model.columnwidths[colname] = width
        self.setColPositions()
        self.redraw()
        self.drawSelectedCol(self.currentcol)
        return

    def get_currentRecord(self):
        """Get the currently selected record"""
        rec = self.model.getRecordAtRow(self.currentrow)
        return rec

    def get_currentColName(self):
        """Get the currently selected record name"""
        colname = self.mo(self.currentcol)
        return colname

    def get_currentRecordName(self):
        """Get the currently selected record name"""
        recname = self.model.getRecName(self.currentrow)
        return recname

    def get_selectedRecordNames(self):
        """Get a list of the current multiple selection, if any"""
        recnames=[]
        for row in self.multiplerowlist:
            recnames.append(self.model.getRecName(row))
        return recnames

    def get_currentRecCol(self):
        """Get the clicked rec and col names as a tuple"""
        recname = self.get_currentRecordName()
        colname = self.get_currentColName()
        return (recname, colname)

    def get_row_clicked(self, event):
        """get row where event on canvas occurs"""

        h=self.rowheight
        #get coord on canvas, not window, need this if scrolling
        y = int(self.canvasy(event.y))
        y_start=self.y_start
        rowc = int((int(y)-y_start)/h)
        return rowc

    def get_col_clicked(self,event):
        """get col where event on canvas occurs"""

        w=self.cellwidth
        x = int(self.canvasx(event.x))
        x_start=self.x_start
        #print self.col_positions
        for colpos in self.col_positions:
            try:
                nextpos=self.col_positions[self.col_positions.index(colpos)+1]
            except:
                nextpos=self.tablewidth
            if x > colpos and x <= nextpos:
                #print 'x=', x, 'colpos', colpos, self.col_positions.index(colpos)
                return self.col_positions.index(colpos)
            else:
                pass
        #return colc

    def setSelectedRow(self, row):
        """Set currently selected row and reset multiple row list"""

        self.currentrow = row
        self.multiplerowlist = []
        self.multiplerowlist.append(row)
        return

    def setSelectedCol(self, col):
        """Set currently selected column"""

        self.currentcol = col
        self.multiplecollist = []
        self.multiplecollist.append(col)
        return

    def setSelectedCells(self, startrow, endrow, startcol, endcol):
        """Set a block of cells selected"""

        self.currentrow = startrow
        self.currentcol = startcol
        if startrow < 0 or startcol < 0:
            return
        if endrow > self.rows or endcol > self.cols:
            return
        for r in range(startrow, endrow):
            self.multiplerowlist.append(r)
        for c in range(startcol, endcol):
            self.multiplecollist.append(c)
        return

    def getSelectedRow(self):
        """Get currently selected row"""
        return self.currentrow

    def getSelectedColumn(self):
        """Get currently selected column"""
        return self.currentcol

    def selectAll(self, evt=None):
        """Select all rows and cells"""

        self.startrow = 0
        self.endrow = self.rows
        self.multiplerowlist = list(range(self.startrow,self.endrow))
        self.drawMultipleRows(self.multiplerowlist)
        self.startcol = 0
        self.endcol = self.cols
        self.multiplecollist = list(range(self.startcol, self.endcol))
        self.drawMultipleCells()
        return

    def getCellCoords(self, row, col):
        """Get x-y coordinates to drawing a cell in a given row/col"""
        colname=self.model.getColumnName(col)
        if colname in self.model.columnwidths:
            w=self.model.columnwidths[colname]
        else:
            w=self.cellwidth
        h=self.rowheight
        x_start=self.x_start
        y_start=self.y_start

        #get nearest rect co-ords for that row/col
        x1=self.col_positions[col]
        y1=y_start+h*row
        x2=x1+w
        y2=y1+h
        return x1,y1,x2,y2

    def getCanvasPos(self, row, col):
        """Get the cell x-y coords as a fraction of canvas size"""
        if self.rows==0:
            return None, None
        x1,y1,x2,y2 = self.getCellCoords(row,col)
        cx=float(x1)/self.tablewidth
        cy=float(y1)/(self.rows*self.rowheight)
        return cx, cy

    def isInsideTable(self,x,y):
        """Returns true if x-y coord is inside table bounds"""
        if self.x_start < x < self.tablewidth and self.y_start < y < self.rows*self.rowheight:
            return 1
        else:
            return 0
        return answer

    def setRowHeight(self, h):
        """Set the row height"""
        self.rowheight = h
        return

    def clearSelected(self):
        """Clear selections"""
        self.delete('rect')
        self.delete('entry')
        self.delete('tooltip')
        self.delete('searchrect')
        self.delete('colrect')
        self.delete('multicellrect')
        return

    def gotoprevRow(self):
        """Programmatically set previous row - eg. for button events"""
        self.clearSelected()
        current = self.getSelectedRow()
        self.setSelectedRow(current-1)
        self.startrow = current-1
        self.endrow = current-1
        #reset multiple selection list
        self.multiplerowlist=[]
        self.multiplerowlist.append(self.currentrow)
        self.drawSelectedRect(self.currentrow, self.currentcol)
        self.drawSelectedRow()
        coltype = self.model.getColumnType(self.currentcol)
        if coltype == 'text' or coltype == 'number':
            self.drawCellEntry(self.currentrow, self.currentcol)
        return

    def gotonextRow(self):
        """Programmatically set next row - eg. for button events"""
        self.clearSelected()
        current = self.getSelectedRow()
        self.setSelectedRow(current+1)
        self.startrow = current+1
        self.endrow = current+1
        #reset multiple selection list
        self.multiplerowlist=[]
        self.multiplerowlist.append(self.currentrow)
        self.drawSelectedRect(self.currentrow, self.currentcol)
        self.drawSelectedRow()
        coltype = self.model.getColumnType(self.currentcol)
        if coltype == 'text' or coltype == 'number':
            self.drawCellEntry(self.currentrow, self.currentcol)
        return

    def handle_left_click(self, event):
        """Respond to a single press"""
        self.clearSelected()
        self.allrows = False
        #which row and column is the click inside?
        rowclicked = self.get_row_clicked(event)
        colclicked = self.get_col_clicked(event)
        if colclicked == None:
            return
        self.focus_set()

        if hasattr(self, 'cellentry'):
            #self.cellentryCallback()
            self.cellentry.destroy()
        #ensure popup menus are removed if present
        if hasattr(self, 'rightmenu'):
            self.rightmenu.destroy()
        if hasattr(self.tablecolheader, 'rightmenu'):
            self.tablecolheader.rightmenu.destroy()

        self.startrow = rowclicked
        self.endrow = rowclicked
        self.startcol = colclicked
        self.endcol = colclicked
        #reset multiple selection list
        self.multiplerowlist=[]
        self.multiplerowlist.append(rowclicked)
        if 0 <= rowclicked < self.rows and 0 <= colclicked < self.cols:
            self.setSelectedRow(rowclicked)
            self.setSelectedCol(colclicked)
            self.drawSelectedRect(self.currentrow, self.currentcol)
            self.drawSelectedRow()
            self.tablerowheader.drawSelectedRows(rowclicked)
            self.tablecolheader.delete('rect')
        if hasattr(self, 'cellentry'):
            self.cellentry.destroy()
        return

    def handle_left_release(self,event):
        self.endrow = self.get_row_clicked(event)
        return

    def handle_left_ctrl_click(self, event):
        """Handle ctrl clicks for multiple row selections"""
        rowclicked = self.get_row_clicked(event)
        colclicked = self.get_col_clicked(event)
        if 0 <= rowclicked < self.rows and 0 <= colclicked < self.cols:
            if rowclicked not in self.multiplerowlist:
                self.multiplerowlist.append(rowclicked)
            else:
                self.multiplerowlist.remove(rowclicked)
            self.drawMultipleRows(self.multiplerowlist)
            if colclicked not in self.multiplecollist:
                self.multiplecollist.append(colclicked)
            self.drawMultipleCells()
        return

    def handle_left_shift_click(self, event):
        """Handle shift click, for selecting multiple rows"""
        self.handle_mouse_drag(event)
        return

    def handle_mouse_drag(self, event):
        """Handle mouse moved with button held down, multiple selections"""
        if hasattr(self, 'cellentry'):
            self.cellentry.destroy()
        rowover = self.get_row_clicked(event)
        colover = self.get_col_clicked(event)
        if colover == None or rowover == None:
            return

        if rowover >= self.rows or self.startrow > self.rows:
            return
        else:
            self.endrow = rowover
        #do columns
        if colover > self.cols or self.startcol > self.cols:
            return
        else:
            self.endcol = colover
            if self.endcol < self.startcol:
                self.multiplecollist=list(range(self.endcol, self.startcol+1))
            else:
                self.multiplecollist=list(range(self.startcol, self.endcol+1))
            #print self.multiplecollist
        #draw the selected rows
        if self.endrow != self.startrow:
            if self.endrow < self.startrow:
                self.multiplerowlist=list(range(self.endrow, self.startrow+1))
            else:
                self.multiplerowlist=list(range(self.startrow, self.endrow+1))
            self.drawMultipleRows(self.multiplerowlist)
            self.tablerowheader.drawSelectedRows(self.multiplerowlist)
            #draw selected cells outline using row and col lists
            #print self.multiplerowlist
            self.drawMultipleCells()
        else:
            self.multiplerowlist = []
            self.multiplerowlist.append(self.currentrow)
            if len(self.multiplecollist) >= 1:
                self.drawMultipleCells()
            self.delete('multiplesel')
        return

    def handle_arrow_keys(self, event):
        """Handle arrow keys press"""
        #print event.keysym

        row = self.get_row_clicked(event)
        col = self.get_col_clicked(event)
        x,y = self.getCanvasPos(self.currentrow, 0)
        if x == None:
            return

        if event.keysym == 'Up':
            if self.currentrow == 0:
                return
            else:
                #self.yview('moveto', y)
                #self.tablerowheader.yview('moveto', y)
                self.currentrow  = self.currentrow -1
        elif event.keysym == 'Down':
            if self.currentrow >= self.rows-1:
                return
            else:
                #self.yview('moveto', y)
                #self.tablerowheader.yview('moveto', y)
                self.currentrow  = self.currentrow +1
        elif event.keysym == 'Right' or event.keysym == 'Tab':
            if self.currentcol >= self.cols-1:
                if self.currentrow < self.rows-1:
                    self.currentcol = 0
                    self.currentrow  = self.currentrow +1
                else:
                    return
            else:
                self.currentcol  = self.currentcol +1
        elif event.keysym == 'Left':
            self.currentcol  = self.currentcol -1
        self.drawSelectedRect(self.currentrow, self.currentcol)
        coltype = self.model.getColumnType(self.currentcol)
        #if coltype == 'text' or coltype == 'number':
        #    self.delete('entry')
        #    self.drawCellEntry(self.currentrow, self.currentcol)
        return

    def handle_double_click(self, event):
        """Do double click stuff. Selected row/cols will already have
           been set with single click binding"""

        row = self.get_row_clicked(event)
        col = self.get_col_clicked(event)
        self.drawCellEntry(self.currentrow, self.currentcol)
        return

    def handle_right_click(self, event):
        """respond to a right click"""

        self.delete('tooltip')
        self.tablerowheader.clearSelected()
        if hasattr(self, 'rightmenu'):
            self.rightmenu.destroy()
        rowclicked = self.get_row_clicked(event)
        colclicked = self.get_col_clicked(event)
        if colclicked == None:
            self.rightmenu = self.popupMenu(event, outside=1)
            return

        if (rowclicked in self.multiplerowlist or self.allrows == True) and colclicked in self.multiplecollist:
            self.rightmenu = self.popupMenu(event, rows=self.multiplerowlist, cols=self.multiplecollist)
        else:
            if 0 <= rowclicked < self.rows and 0 <= colclicked < self.cols:
                self.clearSelected()
                self.allrows = False
                self.setSelectedRow(rowclicked)
                self.setSelectedCol(colclicked)
                self.drawSelectedRect(self.currentrow, self.currentcol)
                self.drawSelectedRow()
            if self.isInsideTable(event.x,event.y) == 1:
                self.rightmenu = self.popupMenu(event,rows=self.multiplerowlist, cols=self.multiplecollist)
            else:
                self.rightmenu = self.popupMenu(event, outside=1)
        return

    def handle_motion(self, event):
        """Handle mouse motion on table"""
        return

    def gotonextCell(self):
        """Move highlighted cell to next cell in row or a new col"""

        if hasattr(self, 'cellentry'):
            self.cellentry.destroy()
        self.currentrow = self.currentrow+1
        if self.currentcol >= self.cols-1:
            self.currentcol = self.currentcol+1
        self.drawSelectedRect(self.currentrow, self.currentcol)
        return

    def movetoSelectedRow(self, row=None, recname=None):
        """Move to selected row, updating table"""

        row=self.model.getRecordIndex(recname)
        self.setSelectedRow(row)
        self.drawSelectedRow()
        x,y = self.getCanvasPos(row, 0)
        self.yview('moveto', y-0.01)
        self.tablecolheader.yview('moveto', y)
        return

    def paste(self, event=None):
        """Copy from clipboard"""
        df = pd.read_clipboard()
        return

    def copy(self, rows, cols=None):
        """Copy cell contents to clipboard"""

        rows = self.multiplerowlist
        if len(rows)<=1:
            rows = list(range(self.rows))
        cols = self.multiplecollist
        df = self.model.df
        data = df.iloc[rows,cols]
        try:
            data.to_clipboard()
        except:
            messagebox.showwarning("Warning",
                                    "No clipboard software.\nInstall xclip",
                                    parent=self.parentframe)
        return

    def transpose(self):
        """Transpose table"""

        self.model.transpose()
        self.updateModel(self.model)
        self.redraw()
        return

    def aggregate(self):
        """Do aggregate operation"""

        df = self.model.df
        cols = list(df.columns)
        funcs = ['mean','sum','size','count','std','first','last','min','max']
        d = MultipleValDialog(title='Aggregate',
                                initialvalues=(cols,funcs,[0,1]),
                                labels=('Group by:','Function:','Replace:'),
                                types=('listbox','combobox','checkbutton'),
                                parent = self.parentframe)
        if d.result == None:
            return
        #apply func
        grp = d.results[0]
        func = d.results[1]
        replace = d.results[2]
        x = df.convert_objects(convert_dates='coerce', convert_numeric=True)
        g = x.groupby(grp).agg(func)
        #replace or make new table
        if replace == True:
            self.model.df = g
            self.showIndex()
            self.redraw()
        else:
            self.createChildTable(g, 'agg-%s-%s' %(grp,func), index=True)
        return

    def pivot(self):
        """Pivot table"""

        self.convertNumeric()
        df = self.model.df
        cols = list(df.columns)
        valcols = list(df.select_dtypes(include=[np.float64,np.int32]))
        d = MultipleValDialog(title='Pivot',
                                initialvalues=(cols,cols,valcols),
                                labels=('Index:', 'Column:', 'Values:'),
                                types=('combobox','combobox','listbox'),
                                tooltips=('a unique index to reshape on','column with variables',
                                    'selecting no values uses all remaining cols'),
                                parent = self.parentframe)
        if d.result == None:
            return
        index = d.results[0]
        column = d.results[1]
        values = d.results[2]
        if values == '': values = None
        elif len(values) == 1: values = values[0]

        p = pd.pivot_table(df, index=index, columns=column, values=values)
        print (p)
        if type(p) is pd.Series:
            p = pd.DataFrame(p)
        self.createChildTable(p, 'pivot-%s-%s' %(index,column), index=True)
        return

    def doCombine(self):
        """Do combine operation"""

        if self.child == None:
            return
        from .dialogs import CombineDialog
        cdlg = CombineDialog(self, df1=self.model.df, df2=self.child.model.df)
        df = cdlg.merged
        if df is None:
            return
        model = TableModel(dataframe=df)
        self.updateModel(model)
        self.redraw()
        return

    def merge(self, table):
        """Merge with another table."""

        df1 = self.model.df
        df2 = table.model.df
        new = pd.merge(df1,df2,left_on=c1,right_on=c2,how=how)
        model = TableModel(new)
        self.updateModel(model)
        self.redraw()
        return

    def describe(self):
        """Create table summary"""

        g = self.model.df.describe()
        self.createChildTable(g)
        return

    def convertColumnNames(self, s='_'):
        """Convert col names so we can use numexpr"""

        d = MultipleValDialog(title='Convert col names',
                                initialvalues=['','',[0,1],[0,1]],
                                labels=['replace spaces with:','add symbol to start',
                                        'make lowercase','make uppercase'],
                                types=('string','string','checkbutton','checkbutton'),
                                parent = self.parentframe)
        if d.result == None:
            return
        sep = d.results[0]
        start = d.results[1]
        lower = d.results[2]
        upper = d.results[3]
        df = self.model.df
        if start != '':
            df.columns = start + df.columns
        if sep != '':
            df.columns = [i.replace(' ',sep) for i in df.columns]
        if lower == 1:
            df.columns = df.columns.str.lower()
        elif upper == 1:
            df.columns = df.columns.str.upper()
        self.redraw()
        return

    def convertNumeric(self):
        """Convert cols to numeric if possible"""
        df = self.model.df
        self.model.df = df.convert_objects(convert_numeric='force')
        self.redraw()
        return

    def createChildTable(self, df, title=None, index=False, out=False):
        """Add the child table"""

        self.closeChildTable()
        if out == True:
            win = Toplevel()
            x,y,w,h = self.getGeometry(self.master)
            win.geometry('+%s+%s' %(int(x+w/2),int(y+h/2)))
            if title != None:
                win.title(title)
        else:
            win = Frame(self.parentframe)
            win.grid(row=self.childrow,column=0,columnspan=2,sticky='news')
        self.childframe = win
        newtable = self.__class__(win, dataframe=df, showtoolbar=0, showstatusbar=1)
        newtable.adjustColumnWidths()
        newtable.show()
        toolbar = ChildToolBar(win, newtable)
        toolbar.grid(row=0,column=3,rowspan=2,sticky='news')
        self.child = newtable
        newtable.pf = self.pf
        if index==True:
            newtable.showIndex()
        return

    def closeChildTable(self):
        """Close the child table"""

        if self.child != None:
            self.child.destroy()
        if hasattr(self, 'childframe'):
            self.childframe.destroy()
        return

    def tableFromSelection(self):
        """Create a new table from the selected cells"""

        df = self.getSelectedDataFrame()
        if len(df) <=1:
            return
        self.createChildTable(df, 'selection')
        return

    def showasText(self):
        """Get table as formatted text - for printing"""

        d = MultipleValDialog(title='Table to Text',
                                initialvalues=(['left','right'],[1,0],[1,0],[0,1],''),
                                labels=['justify:','header ','include index:','sparsify:','na_rep:'],
                                types=('combobox','checkbutton','checkbutton','checkbutton','string'),
                                parent = self.parentframe)
        if d.result == None:
            return
        justify = d.results[0]
        header = d.results[0]
        index = d.results[2]
        sparsify = d.results[3]
        na_rep = d.results[4]

        df = self.model.df
        s = df.to_string(justify=justify,header=header,index=index,sparsify=sparsify,na_rep=na_rep)
        from tkinter.scrolledtext import ScrolledText
        from .dialogs import SimpleEditor
        w = Toplevel(self.parentframe)
        w.grab_set()
        w.transient(self)
        ed = SimpleEditor(w)
        ed.pack(in_=w, fill=BOTH, expand=Y)
        ed.text.insert(END, s)
        return

    # --- Some cell specific actions here ---

    def popupMenu(self, event, rows=None, cols=None, outside=None):
        """Add left and right click behaviour for canvas, should not have to override
            this function, it will take its values from defined dicts in constructor"""

        defaultactions = {
                        "Copy" : lambda: self.copy(rows, cols),
                        #"Paste" : lambda: self.paste(rows, cols),
                        #"Fill Down" : lambda: self.fillDown(rows, cols),
                        #"Fill Right" : lambda: self.fillAcross(cols, rows),
                        "Add Row(s)" : lambda: self.addRows(),
                        "Delete Row(s)" : lambda: self.deleteRow(),
                        "Add Column(s)" : lambda: self.addColumn(),
                        "Delete Column(s)" : lambda: self.deleteColumn(),
                        "Clear Data" : lambda: self.deleteCells(rows, cols),
                        "Select All" : self.selectAll,
                        #"Auto Fit Columns" : self.autoResizeColumns,
                        "Show as Text" : self.showasText,
                        "Filter Records" : self.queryBar,
                        "New": self.new,
                        "Load": self.load,
                        "Save": self.save,
                        "Save as": self.saveAs,
                        "Import csv": lambda: self.importCSV(dialog=True),
                        "Plot Selected" : self.plotSelected,
                        "Hide plot" : self.hidePlot,
                        "Preferences" : self.showPrefs}

        main = ["Copy", #"Fill Down","Fill Right",
                "Clear Data", "Delete Row(s)", "Delete Column(s)"]
        general = ["Add Row(s)", "Add Column(s)", "Select All", "Filter Records",
                    "Show as Text", "Preferences"]

        filecommands = ['New','Load','Import csv','Save','Save as']
        plotcommands = ['Plot Selected','Hide plot']

        def createSubMenu(parent, label, commands):
            menu = Menu(parent, tearoff = 0)
            popupmenu.add_cascade(label=label,menu=menu)
            for action in commands:
                menu.add_command(label=action, command=defaultactions[action])
            return menu

        def add_commands(fieldtype):
            """Add commands to popup menu for column type and specific cell"""
            functions = self.columnactions[fieldtype]
            for f in list(functions.keys()):
                func = getattr(self, functions[f])
                popupmenu.add_command(label=f, command= lambda : func(row,col))
            return

        popupmenu = Menu(self, tearoff = 0)
        def popupFocusOut(event):
            popupmenu.unpost()

        if outside == None:
            #if outside table, just show general items
            row = self.get_row_clicked(event)
            col = self.get_col_clicked(event)
            coltype = self.model.getColumnType(col)
            def add_defaultcommands():
                """now add general actions for all cells"""
                for action in main:
                    if action == 'Fill Down' and (rows == None or len(rows) <= 1):
                        continue
                    if action == 'Fill Right' and (cols == None or len(cols) <= 1):
                        continue
                    else:
                        popupmenu.add_command(label=action, command=defaultactions[action])
                return

            if coltype in self.columnactions:
                add_commands(coltype)
            add_defaultcommands()

        for action in general:
            popupmenu.add_command(label=action, command=defaultactions[action])

        popupmenu.add_separator()
        createSubMenu(popupmenu, 'File', filecommands)
        createSubMenu(popupmenu, 'Plot', plotcommands)
        popupmenu.bind("<FocusOut>", popupFocusOut)
        popupmenu.focus_set()
        popupmenu.post(event.x_root, event.y_root)
        return popupmenu

    # --- spreadsheet type functions ---

    def fillDown(self, rowlist, collist):
        """Fill down a column, or multiple columns"""
        model = self.model
        #remove first element as we don't want to overwrite it
        rowlist.remove(rowlist[0])

        self.redraw()
        return

    def fillAcross(self, collist, rowlist):
        """Fill across a row, or multiple rows"""
        model = self.model
        frstcol = collist[0]
        collist.remove(frstcol)

        self.redraw()
        return

    def getSelectionValues(self):
        """Get values for current multiple cell selection"""
        if len(self.multiplerowlist) == 0 or len(self.multiplecollist) == 0:
            return None
        rows = self.multiplerowlist
        cols = self.multiplecollist
        model = self.model
        if len(rows)<1 or len(cols)<1:
            return None
        #if only one row selected we plot whole col
        if len(rows) == 1:
            rows = self.rowrange
        lists = []

        for c in cols:
            x=[]
            for r in rows:
                #absr = self.get_AbsoluteRow(r)
                val = model.getValueAt(r,c)
                if val == None or val == '':
                    continue
                x.append(val)
            lists.append(x)
        return lists

    def showPlotViewer(self, parent=None):
        if not hasattr(self, 'pf'):
            self.pf = PlotViewer(table=self, parent=parent)
        return self.pf

    def hidePlot(self):
        """Hide plot frame"""
        if hasattr(self, 'pf'):
            self.pf.quit()
            self.pf = None
        return

    def getSelectedDataFrame(self):
        """Return a sub-dataframe of the selected cells"""
        df = self.model.df
        rows = self.multiplerowlist
        if len(rows)<=1:
            rows = list(range(self.rows))
        cols = self.multiplecollist
        data = df.iloc[rows,cols]
        return data

    def getPlotData(self):
        """Plot data from selection"""
        data = self.getSelectedDataFrame()
        #data.sort(inplace=True)
        #if the first col is text we try to use it as an index
        #if data.dtypes[0] == 'object':
        #    data.set_index(data.columns[0], inplace=True)
        data = data.convert_objects(convert_numeric='force')
        return data

    def plotSelected(self):
        """Plot the selected data in the associated plotviewer"""

        if not hasattr(self, 'pf') or self.pf == None:
            self.pf = PlotViewer(table=self)
        else:
            if type(self.pf.main) is tkinter.Toplevel:
                self.pf.main.deiconify()
        data = self.getPlotData()
        self.pf.data = data
        self.pf.plotCurrent()
        return

    def plot3D(self):

        if not hasattr(self, 'pf'):
            self.pf = PlotViewer(table=self)

        data = self.getPlotData()
        self.pf.data = data
        self.pf.plot3D()
        return

    #--- Drawing stuff ---

    def drawGrid(self, startrow, endrow):
        """Draw the table grid lines"""
        self.delete('gridline','text')
        rows=len(self.rowrange)
        cols=self.cols
        w = self.cellwidth
        h = self.rowheight
        x_start=self.x_start
        y_start=self.y_start
        x_pos=x_start

        if self.vertlines==1:
            for col in range(cols+1):
                x=self.col_positions[col]
                self.create_line(x,y_start,x,y_start+rows*h, tag='gridline',
                                     fill=self.grid_color, width=self.linewidth)
        if self.horizlines==1:
            for row in range(startrow, endrow+1):
                y_pos=y_start+row*h
                self.create_line(x_start,y_pos,self.tablewidth,y_pos, tag='gridline',
                                    fill=self.grid_color, width=self.linewidth)
        return

    def drawRowHeader(self):
        """User has clicked to select a cell"""
        self.delete('rowheader')
        x_start=self.x_start
        y_start=self.y_start
        h=self.rowheight
        rowpos=0
        for row in self.rowrange:
            x1,y1,x2,y2 = self.getCellCoords(rowpos,0)
            self.create_rectangle(0,y1,x_start-2,y2,
                                      fill='gray75',
                                      outline='white',
                                      width=1,
                                      tag='rowheader')
            self.create_text(x_start/2,y1+h/2,
                                      text=row+1,
                                      fill='black',
                                      font=self.thefont,
                                      tag='rowheader')
            rowpos+=1
        return

    def drawSelectedRect(self, row, col, color=None):
        """User has clicked to select a cell"""
        if col >= self.cols:
            return
        self.delete('currentrect')
        #bg = self.selectedcolor
        if color == None:
            color = 'gray25'
        w=2
        x1,y1,x2,y2 = self.getCellCoords(row,col)
        rect = self.create_rectangle(x1+w/2+1,y1+w/2+1,x2-w/2,y2-w/2,
                                  outline=color,
                                  width=w,
                                  tag='currentrect')
        #raise text above all
        self.lift('celltext'+str(col)+'_'+str(row))
        return

    def drawRect(self, row, col, color=None, tag=None, delete=1):
        """Cell is colored"""
        if delete==1:
            self.delete('cellbg'+str(row)+str(col))
        if color==None or color==self.cellbackgr:
            return
        else:
            bg=color
        if tag==None:
            recttag='fillrect'
        else:
            recttag=tag
        w=1
        x1,y1,x2,y2 = self.getCellCoords(row,col)
        rect = self.create_rectangle(x1+w/2,y1+w/2,x2-w/2,y2-w/2,
                                  fill=bg,
                                  outline=bg,
                                  width=w,
                                  tag=(recttag,'cellbg'+str(row)+str(col)))
        self.lower(recttag)
        return

    def cellentryCallback(self, row, col):
        """Callback for cell entry"""
        value = self.cellentryvar.get()
        self.model.setValueAt(value,row,col)
        self.drawText(row, col, value, align=self.align)
        self.delete('entry')
        self.gotonextCell()
        return

    def drawCellEntry(self, row, col, text=None):
        """When the user single/double clicks on a text/number cell,
          bring up entry window and allow edits."""

        if self.editable == False:
            return
        h = self.rowheight
        model = self.model
        text = self.model.getValueAt(row, col)
        x1,y1,x2,y2 = self.getCellCoords(row,col)
        w=x2-x1
        self.cellentryvar = txtvar = StringVar()
        txtvar.set(text)

        self.cellentry = Entry(self.parentframe,width=20,
                        textvariable=txtvar,
                        takefocus=1,
                        font=self.thefont)
        self.cellentry.icursor(END)
        self.cellentry.bind('<Return>', lambda x: self.cellentryCallback(row,col))
        self.cellentry.focus_set()
        self.entrywin = self.create_window(x1,y1,
                                width=w,height=h,
                                window=self.cellentry,anchor='nw',
                                tag='entry')
        return

    def checkDataEntry(self,event=None):
        """do validation checks on data entry in a widget"""

        #if user enters commas, change to points
        value=event.widget.get()
        if value!='':
            try:
                value=re.sub(',','.', value)
                value=float(value)

            except ValueError:
                event.widget.configure(bg='red')
                return 0
        elif value == '':
            return 1
        return 1

    def drawText(self, row, col, celltxt, align=None):
        """Draw the text inside a cell area"""

        self.delete('celltext'+str(col)+'_'+str(row))
        h = self.rowheight
        x1,y1,x2,y2 = self.getCellCoords(row,col)
        w=x2-x1
        wrap = False
        pad=5
        if type(celltxt) is np.float64:
            celltxt = np.round(celltxt,3)
        celltxt = str(celltxt)
        length = len(celltxt)
        if length == 0:
            return
        #if cell width is less than x, print nothing
        if w<=10:
            return
        if w < 18:
            celltxt = '.'
            return

        fgcolor = 'black'
        if align == None:
            align = 'center'
        elif align == 'w':
            x1 = x1-w/2+pad
        elif align == 'e':
            x1 = x1+w/2-pad

        fontsize = self.fontsize
        colname = self.model.getColumnName(col)
        #scaling between canvas and text normalised to about font 14
        scale = 8.5 * float(fontsize)/12
        size = length * scale
        if size > w:
            newlength = w / scale
            #print w, size, length, newlength
            celltxt = celltxt[0:int(math.floor(newlength))]

        rect = self.create_text(x1+w/2,y1+h/2,
                                  text=celltxt,
                                  fill=fgcolor,
                                  font=self.thefont,
                                  anchor=align,
                                  tag=('text','celltext'+str(col)+'_'+str(row)))
        return

    def drawSelectedRow(self):
        """Draw the highlight rect for the currently selected row"""
        self.delete('rowrect')
        row = self.currentrow
        x1,y1,x2,y2 = self.getCellCoords(row,0)
        x2 = self.tablewidth
        rect = self.create_rectangle(x1,y1,x2,y2,
                                  fill=self.rowselectedcolor,
                                  outline=self.rowselectedcolor,
                                  tag='rowrect')
        self.lower('rowrect')
        self.lower('fillrect')
        self.tablerowheader.drawSelectedRows(self.currentrow)
        return

    def drawSelectedCol(self, col=None, delete=1):
        """Draw an outline rect fot the current column selection"""
        if delete == 1:
            self.delete('colrect')
        if col == None:
            col = self.currentcol
        w=2
        x1,y1,x2,y2 = self.getCellCoords(0,col)
        y2 = self.rows * self.rowheight
        rect = self.create_rectangle(x1+w/2,y1+w/2,x2,y2+w/2,
                                     width=w,fill='#F8E0E6',outline='',
                                     tag='colrect')
        self.lower('colrect')
        self.lower('rowrect')
        self.delete('currentrect')
        return

    def drawMultipleRows(self, rowlist):
        """Draw more than one row selection"""
        self.delete('multiplesel')
        for r in rowlist:
            if r not in self.visiblerows or r > self.rows-1:
                continue
            x1,y1,x2,y2 = self.getCellCoords(r,0)
            x2 = self.tablewidth
            rect = self.create_rectangle(x1,y1,x2,y2,
                                      fill=self.multipleselectioncolor,
                                      outline=self.rowselectedcolor,
                                      tag=('multiplesel','rowrect'))
        self.lower('multiplesel')
        self.lower('fillrect')
        return

    def drawMultipleCells(self):
        """Draw an outline box for multiple cell selection"""
        self.delete('multicellrect')
        rows = self.multiplerowlist
        cols = self.multiplecollist
        w=2
        x1,y1,a,b = self.getCellCoords(rows[0],cols[0])
        c,d,x2,y2 = self.getCellCoords(rows[len(rows)-1],cols[len(cols)-1])
        rect = self.create_rectangle(x1+w/2,y1+w/2,x2,y2,
                             outline=self.boxoutlinecolor, width=w,
                             tag='multicellrect')

        return

    def setcellbackgr(self):
        clr = self.getaColor(self.cellbackgr)
        if clr != None:
            self.cellbackgr = clr
        return

    def setgrid_color(self):
        clr = self.getaColor(self.grid_color)
        if clr != None:
            self.grid_color = clr

        return

    def setrowselectedcolor(self):
        clr = self.getaColor(self.rowselectedcolor)
        if clr != None:
            self.rowselectedcolor = clr
        return

    def getaColor(self, oldcolor):
        import tkinter.colorchooser
        ctuple, newcolor = tkinter.colorchooser.askcolor(title='pick a color', initialcolor=oldcolor,
                                                   parent=self.parentframe)
        if ctuple == None:
            return None
        return str(newcolor)

    #--- Preferences stuff ---

    def showPrefs(self, prefs=None):
        """Show table options dialog using an instance of prefs"""

        if self.prefs == None:
            self.loadPrefs()
        self.prefswindow=Toplevel()
        x,y,w,h = self.getGeometry(self.master)
        #self.prefswindow.geometry('+%s+%s' %(x+w/2,y+h/2))
        self.prefswindow.title('Preferences')
        self.prefswindow.resizable(width=FALSE, height=FALSE)
        self.prefswindow.grab_set()
        self.prefswindow.transient(self)

        frame1=Frame(self.prefswindow)
        frame1.pack(side=LEFT)
        frame2=Frame(self.prefswindow)
        frame2.pack()
        def close_prefsdialog():
            self.prefswindow.destroy()
        row=0
        Checkbutton(frame1, text="Show horizontal lines", variable=self.horizlinesvar,
                    onvalue=1, offvalue=0).grid(row=row,column=0, columnspan=2, sticky='news')
        row=row+1
        Checkbutton(frame1, text="Show vertical lines", variable=self.vertlinesvar,
                    onvalue=1, offvalue=0).grid(row=row,column=0, columnspan=2, sticky='news')
        row=row+1
        Checkbutton(frame1, text="Alternate Row Color", variable=self.alternaterowsvar,
                    onvalue=1, offvalue=0).grid(row=row,column=0, columnspan=2, sticky='news')
        row=row+1
        lblrowheight = Label(frame1,text='Row Height:')
        lblrowheight.grid(row=row,column=0,padx=3,pady=2)
        rowheightentry = tkinter.Scale(frame1,from_=12,to=50,resolution=1,orient='horizontal',
                            variable=self.rowheightvar)
        rowheightentry.grid(row=row,column=1)
        row=row+1
        lblcellwidth = Label(frame1,text='Cell Width:')
        lblcellwidth.grid(row=row,column=0,padx=3,pady=2)
        cellwidthentry = tkinter.Scale(frame1,from_=20,to=500,resolution=10,orient='horizontal',
                            variable=self.cellwidthvar)
        cellwidthentry.grid(row=row,column=1)
        row=row+1

        lbllinewidth = Label(frame1,text='Line Width:')
        lbllinewidth.grid(row=row,column=0,padx=3,pady=2)
        linewidthentry = tkinter.Scale(frame1,from_=0,to=10,resolution=1,orient='horizontal',
                            variable=self.linewidthvar)
        linewidthentry.grid(row=row,column=1)
        row=row+1

        rowhdrwidth=Label(frame1,text='Row Header Width:')
        rowhdrwidth.grid(row=row,column=0,padx=3,pady=2)
        rowhdrentry = tkinter.Scale(frame1,from_=0,to=300,resolution=10,orient='horizontal',
                                    variable=self.rowheaderwidthvar)
        rowhdrentry.grid(row=row,column=1)
        row=row+1

        #fonts
        fts = self.getFonts()
        Label(frame2,text='font').grid(row=row,column=0)
        fb = Combobox(frame2, values=fts,
                       textvariable=self.fontvar)
        #currfont = self.prefs.get('celltextfont')
        fb.grid(row=row,column=1, columnspan=2, sticky='nes', padx=3,pady=2)
        row=row+1

        lblfontsize = Label(frame2,text='Text Size:')
        lblfontsize.grid(row=row,column=0,padx=3,pady=2)
        fontsizeentry = tkinter.Scale(frame2,from_=6,to=50,resolution=1,orient='horizontal',
                                variable=self.celltextsizevar)

        fontsizeentry.grid(row=row,column=1, sticky='wens',padx=3,pady=2)
        row=row+1

        #cell alignment
        lbl=Label(frame2,text='Alignment:')
        lbl.grid(row=row,column=0,padx=3,pady=2)

        alignments=['center','w','e']
        alignentry_button = Combobox(frame2, values=alignments,
                              textvariable=self.cellalignvar)
        alignentry_button.grid(row=row,column=1, sticky='nes', padx=3,pady=2)
        row=row+1

        #colors
        style = Style()
        style.configure("cb.TButton", background=self.cellbackgr)
        cellbackgrbutton = Button(frame2, text='table background',style="cb.TButton",
                                  command=self.setcellbackgr)

        cellbackgrbutton.grid(row=row,column=0,columnspan=2, sticky='news')
        row=row+1
        style = Style()
        style.configure("gc.TButton", background=self.grid_color)
        grid_colorbutton = Button(frame2, text='grid color', style="gc.TButton",
                                command=self.setgrid_color)
        grid_colorbutton.grid(row=row,column=0,columnspan=2, sticky='news')
        row=row+1
        style = Style()
        style.configure("rhc.TButton", background=self.rowselectedcolor)
        rowselectedcolorbutton = Button(frame2, text='row highlight color', style="rhc.TButton",
                                command=self.setrowselectedcolor)
        rowselectedcolorbutton.grid(row=row,column=0,columnspan=2, sticky='news')
        row=row+1

        frame=Frame(self.prefswindow)
        frame.pack(fill=BOTH,expand=1)
        # Apply Button
        b = Button(frame, text="Apply Settings", command=self.applyPrefs)
        b.pack(side=LEFT,expand=1)

        # Close button
        c=Button(frame,text='Close', command=close_prefsdialog)
        c.pack(side=LEFT,expand=1)
        self.prefswindow.focus_set()
        self.prefswindow.grab_set()
        self.prefswindow.wait_window()
        return self.prefswindow

    def getFonts(self):
        fonts = set(list(tkinter.font.families()))
        fonts = sorted(list(fonts))
        return fonts

    def loadPrefs(self, prefs=None):
        """Load table specific prefs from the prefs instance used
           if they are ntafa99
           ot present, create them."""

        if prefs==None:
            prefs=Preferences('Table',{'check_for_update':1})
        self.prefs = prefs
        defaultprefs = {'horizlines':self.horizlines, 'vertlines':self.vertlines,
                        'alternaterows':self.alternaterows,
                        'rowheight':self.rowheight,
                        'cellwidth':80,
                        'autoresizecols': 0,
                        'align': 'w',
                        'celltextsize':10, 'celltextfont':'Arial',
                        'cellbackgr': self.cellbackgr, 'grid_color': self.grid_color,
                        'linewidth' : self.linewidth,
                        'rowselectedcolor': self.rowselectedcolor,
                        'rowheaderwidth': self.rowheaderwidth}

        for prop in list(defaultprefs.keys()):
            try:
                self.prefs.get(prop);
            except:
                self.prefs.set(prop, defaultprefs[prop])
        self.defaultprefs = defaultprefs

        #Create tkvars for dialog
        self.fontvar = StringVar()
        self.fontvar.set(self.prefs.get('celltextfont'))
        self.rowheightvar = IntVar()
        self.rowheightvar.set(self.prefs.get('rowheight'))
        self.rowheight = self.rowheightvar.get()
        self.cellwidthvar = IntVar()
        self.cellwidthvar.set(self.prefs.get('cellwidth'))
        self.cellwidth = self.cellwidthvar.get()
        self.cellalignvar = StringVar()
        self.cellalignvar.set(self.prefs.get('align'))
        self.align = self.cellalignvar.get()
        self.linewidthvar = IntVar()
        self.linewidthvar.set(self.prefs.get('linewidth'))
        self.horizlinesvar = IntVar()
        self.horizlinesvar.set(self.prefs.get('horizlines'))
        self.vertlinesvar = IntVar()
        self.vertlinesvar.set(self.prefs.get('vertlines'))
        self.alternaterowsvar = IntVar()
        self.alternaterowsvar.set(self.prefs.get('alternaterows'))
        self.celltextsizevar = IntVar()
        self.celltextsizevar.set(self.prefs.get('celltextsize'))
        self.cellbackgr = self.prefs.get('cellbackgr')
        self.grid_color = self.prefs.get('grid_color')
        self.rowselectedcolor = self.prefs.get('rowselectedcolor')
        self.fontsize = self.celltextsizevar.get()
        self.thefont = (self.prefs.get('celltextfont'), self.prefs.get('celltextsize'))
        self.rowheaderwidthvar = IntVar()
        self.rowheaderwidthvar.set(self.prefs.get('rowheaderwidth'))
        self.rowheaderwidth = self.rowheaderwidthvar.get()
        return

    def savePrefs(self):
        """Save and set the prefs"""
        try:
            self.prefs.set('horizlines', self.horizlinesvar.get())
            self.horizlines = self.horizlinesvar.get()
            self.prefs.set('vertlines', self.vertlinesvar.get())
            self.vertlines = self.vertlinesvar.get()
            self.prefs.set('alternaterows', self.alternaterowsvar.get())
            self.alternaterows = self.alternaterowsvar.get()
            self.prefs.set('rowheight', self.rowheightvar.get())
            self.rowheight = self.rowheightvar.get()
            self.prefs.set('cellwidth', self.cellwidthvar.get())
            self.cellwidth = self.cellwidthvar.get()
            self.prefs.set('align', self.cellalignvar.get())
            self.align = self.cellalignvar.get()
            self.prefs.set('linewidth', self.linewidthvar.get())
            self.linewidth = self.linewidthvar.get()
            self.prefs.set('celltextsize', self.celltextsizevar.get())
            self.prefs.set('celltextfont', self.fontvar.get())
            self.prefs.set('cellbackgr', self.cellbackgr)
            self.prefs.set('grid_color', self.grid_color)
            self.prefs.set('rowselectedcolor', self.rowselectedcolor)
            self.prefs.set('rowheaderwidth', self.rowheaderwidth)
            self.rowheaderwidth = self.rowheaderwidthvar.get()
            self.thefont = (self.prefs.get('celltextfont'), self.prefs.get('celltextsize'))
            self.fontsize = self.prefs.get('celltextsize')

        except ValueError:
            pass
        self.prefs.save_prefs()
        return

    def applyPrefs(self):
        """Apply prefs to the table by redrawing"""
        self.savePrefs()
        self.redraw()
        return

    def show_progressbar(self,message=None):
        """Show progress bar window for loading of data"""
        progress_win=Toplevel() # Open a new window
        progress_win.title("Please Wait")
        #progress_win.geometry('+%d+%d' %(self.parentframe.rootx+200,self.parentframe.rooty+200))
        #force on top
        progress_win.grab_set()
        progress_win.transient(self.parentframe)
        if message==None:
            message='Working'
        lbl = Label(progress_win,text=message,font='Arial 16')

        lbl.grid(row=0,column=0,columnspan=2,sticky='news',padx=6,pady=4)
        progrlbl = Label(progress_win,text='Progress:')
        progrlbl.grid(row=1,column=0,sticky='news',padx=2,pady=4)
        import ProgressBar
        self.bar = ProgressBar.ProgressBar(progress_win)
        self.bar.frame.grid(row=1,column=1,columnspan=2,padx=2,pady=4)

        return progress_win

    def updateModel(self, model):
        """Should call this method when a new table model is loaded"""

        self.model = model
        self.rows = self.model.getRowCount()
        self.cols = self.model.getColumnCount()
        self.tablewidth = (self.cellwidth)*self.cols
        self.tablecolheader.destroy()
        self.tablerowheader.destroy()
        self.show()
        return

    def new(self):
        """Clears all the data and makes a new table"""

        mpDlg = MultipleValDialog(title='Create new table',
                                    initialvalues=(50, 10),
                                    labels=('rows','columns'),
                                    types=('int','int'),
                                    parent=self.parentframe)

        if mpDlg.result == True:
            rows = mpDlg.results[0]
            cols = mpDlg.results[1]
            model = TableModel(rows=rows,columns=cols)
            self.updateModel(model)
        return

    def load(self, filename=None):
        """load from a file"""
        if filename == None:
            filename = filedialog.askopenfilename(parent=self.master,
                                                      defaultextension='.mpk',
                                                      initialdir=os.getcwd(),
                                                      filetypes=[("msgpack","*.mpk"),
                                                        ("All files","*.*")])
        if not os.path.exists(filename):
            print('file does not exist')
            return
        if filename:
            model = TableModel()
            model.load(filename)
            self.updateModel(model)
            self.filename = filename
            self.adjustColumnWidths()
            self.redraw()
        return

    def saveAs(self, filename=None):
        """Save dataframe to file"""

        if filename == None:
            filename = filedialog.asksaveasfilename(parent=self.master,
                                                     #defaultextension='.mpk',
                                                     initialdir = self.currentdir,
                                                     filetypes=[("msgpack","*.mpk"),
                                                                    ("csv","*.csv"),
                                                                    ("excel","*.xls"),
                                                                    ("html","*.html"),
                                                      ("All files","*.*")])
        if filename:
            self.model.save(filename)
            self.filename = filename
            self.currentdir = os.path.basename(filename)
        return

    def save(self):
        self.saveAs(self.filename)
        return

    def importCSV(self, filename=None, dialog=False):
        """Import from csv file"""
        if filename == None:
            filename = filedialog.askopenfilename(parent=self.master,
                                                          defaultextension='.csv',
                                                          initialdir=os.getcwd(),
                                                          filetypes=[("csv","*.csv"),
                                                                     ("tsv","*.tsv"),
                                                                     ("txt","*.txt"),
                                                            ("All files","*.*")])
        if not filename:
            return
        if dialog == True:
            impdialog = ImportDialog(self, filename=filename)
            df = impdialog.df
            if df is None:
                return
        else:
            df = pd.read_csv(filename)
        model = TableModel(dataframe=df)
        self.updateModel(model)
        self.redraw()
        if hasattr(self, 'pf'):
            self.pf.updateData()
        return

    def loadExcel(self, filename=None):
        """Load excel file"""
        if filename == None:
            filename = filedialog.askopenfilename(parent=self.master,
                                                          defaultextension='.xls',
                                                          initialdir=os.getcwd(),
                                                          filetypes=[("xls","*.xls"),
                                                                     ("xlsx","*.xlsx"),
                                                            ("All files","*.*")])
        if not filename:
            return
        df = pd.read_excel(filename,sheetname=0)
        model = TableModel(dataframe=df)
        self.updateModel(model)
        return

    def doExport(self, filename=None):
        """Do a simple export of the cell contents to csv"""
        if filename == None:
            filename = filedialog.asksaveasfilename(parent=self.master,
                                                      defaultextension='.csv',
                                                      initialdir = os.getcwd(),
                                                      filetypes=[("csv","*.csv"),
                                                        ("All files","*.*")])
        if filename:
            df = self.model.df
            df.to_csv(filename)
        return

    @classmethod
    def checkOS(cls):
        """Check the OS we are in"""
        from sys import platform as _platform
        if _platform == "linux" or _platform == "linux2":
            return 'linux'
        elif _platform == "darwin":
            return 'darwin'
        if "win" in _platform:
            return 'windows'

    def getGeometry(self, frame):
        """Get frame geometry"""
        return frame.winfo_rootx(), frame.winfo_rooty(), frame.winfo_width(), frame.winfo_height()


class AutoScrollbar(Scrollbar):
    """a scrollbar that hides itself if it's not needed.  only
       works if you use the grid geometry manager."""
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise TclError("cannot use place with this widget")

class ToolBar(Frame):
    """Uses the parent instance to provide the functions"""
    def __init__(self, parent=None, parentapp=None):

        Frame.__init__(self, parent, width=600, height=40)
        self.parentframe = parent
        self.parentapp = parentapp
        img = images.open_proj()
        self.addButton('Load table', self.parentapp.load, img, 'load table')
        img = images.save_proj()
        self.addButton('Save', self.parentapp.save, img, 'save')
        img = images.importcsv()
        func = lambda: self.parentapp.importCSV(dialog=1)
        self.addButton('Import', func, img, 'import csv')
        img = images.excel()
        self.addButton('Load excel', self.parentapp.loadExcel, img, 'load excel file')
        img = images.plot()
        self.addButton('Plot', self.parentapp.plotSelected, img, 'plot selected')
        img = images.transpose()
        self.addButton('Transpose', self.parentapp.transpose, img, 'transpose')
        img = images.aggregate()
        self.addButton('Aggregate', self.parentapp.aggregate, img, 'aggregate')
        img = images.pivot()
        self.addButton('Pivot', self.parentapp.pivot, img, 'pivot')
        img = images.merge()
        self.addButton('Merge', self.parentapp.doCombine, img, 'merge, concat or join')
        img = images.table_multiple()
        self.addButton('Table from selection', self.parentapp.tableFromSelection,
                    img, 'sub-table from selection')
        img = images.filtering()
        self.addButton('Query', self.parentapp.queryBar, img, 'filter table')
        img = images.function()
        self.addButton('Evaluate function', self.parentapp.evalBar, img, 'apply a function')
        img = images.table_delete()
        self.addButton('Clear', self.parentapp.clearTable, img, 'clear table')
        img = images.prefs()
        self.addButton('Prefs', self.parentapp.showPrefs, img, 'table preferences')
        return

    def addButton(self, name, callback, img=None, tooltip=None):
        if img==None:
            b = Button(self, text=name, command=callback)
        else:
            b = Button(self, text=name, command=callback,
                             image=img)
        b.image = img
        b.pack(side=TOP)
        if tooltip != None:
            ToolTip.createToolTip(b, tooltip)
        return

class ChildToolBar(ToolBar):
    """Smaller toolbar for child table"""
    def __init__(self, parent=None, parentapp=None):
        Frame.__init__(self, parent, width=600, height=40)
        self.parentframe = parent
        self.parentapp = parentapp
        img = images.open_proj()
        self.addButton('Load table', self.parentapp.load, img, 'load table')
        img = images.importcsv()
        func = lambda: self.parentapp.importCSV(dialog=1)
        self.addButton('Import', func, img, 'import csv')
        img = images.plot()
        self.addButton('Plot', self.parentapp.plotSelected, img, 'plot selected')
        img = images.table_delete()
        self.addButton('Clear', self.parentapp.clearTable, img, 'clear table')
        img = images.cross()
        self.addButton('Close', self.parentapp.remove, img, 'close')
        return

class statusBar(Frame):
    """Status bar class"""
    def __init__(self, parent=None, parentapp=None):

        Frame.__init__(self, parent)
        self.parentframe = parent
        self.parentapp = parentapp
        sfont = ("Helvetica bold", 11)
        clr = '#A10000'
        self.rowsvar = StringVar()
        l=Label(self,textvariable=self.rowsvar,font=sfont,foreground=clr)
        l.pack(fill=X, side=LEFT)
        Label(self,text='rows x',font=sfont,foreground=clr).pack(side=LEFT)
        self.colsvar = StringVar()
        self.colsvar.set(len(self.parentapp.model.df))
        l=Label(self,textvariable=self.colsvar,font=sfont,foreground=clr)
        l.pack(fill=X, side=LEFT)
        Label(self,text='columns',font=sfont,foreground=clr).pack(side=LEFT)
        return

    def update(self):
        model = self.parentapp.model
        self.rowsvar.set(len(model.df))
        self.colsvar.set(len(model.df.columns))
        return

