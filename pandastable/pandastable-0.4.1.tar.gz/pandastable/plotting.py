#!/usr/bin/env python
"""
    Module for pylab plotting helper classes.

    Created Jan 2014
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import types
from tkinter import *
from tkinter.ttk import *
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.animation as animation
from collections import OrderedDict
import operator
from .dialogs import *

colormaps = sorted(m for m in plt.cm.datad if not m.endswith("_r"))

class PlotViewer(Frame):
    """Provides a frame for figure canvas and MPL settings"""

    def __init__(self, table, parent=None):

        self.parent=parent
        self.table=table
        self.table.pf = self #opaque ref
        self.mode = 0
        if self.parent != None:
            Frame.__init__(self, parent)
            self.main = self.master
        else:
            self.main = Toplevel()
            self.master = self.main
            self.main.title('Plot Viewer')
            self.main.protocol("WM_DELETE_WINDOW", self.quit)
        self.addFigure(self.main)
        def hide():
            if hidevar.get():
                self.nb.pack_forget()
            else:
                self.nb.pack(side=TOP,fill=BOTH)
        bf = Frame(self.main, padding=2)
        bf.pack(side=TOP,fill=BOTH)
        b = Button(bf, text="Apply", command=self.applyPlotoptions)
        b.pack(side=LEFT,fill=X,expand=1)
        hidevar = IntVar()
        c = Checkbutton(bf,text='Hide Options', command=hide, variable=hidevar)
        c.pack(side=LEFT,fill=X,expand=1)
        self.nb = Notebook(self.main)
        self.nb.bind('<<NotebookTabChanged>>', self.setMode)
        self.nb.pack(side=TOP,fill=BOTH)

        self.mplopts = MPLBaseOptions(parent=self)
        w1 = self.mplopts.showDialog(self.nb)
        self.nb.add(w1, text='base plot options', sticky='news')
        self.mplopts3d = MPL3DOptions(parent=self)
        w2 = self.mplopts3d.showDialog(self.nb)
        self.nb.add(w2, text='3D plot', sticky='news')
        '''if self._importSeaborn() == 1:
            self.factorplotter = FactorPlotter()
            w3 = self.factorplotter.showDialog(self.nb)
            self.nb.add(w3, text='factor plots', sticky='news')'''
        return

    def _importSeaborn(self):
        """Try to import seaborn. If not installed return false"""
        try:
            import seaborn as sns
            return 1
        except:
            print('seaborn not installed')
            return 0

    def setMode(self, evt=None):
        """Set the plot mode based on selected tab"""
        self.mode = self.nb.index(self.nb.select())
        return

    def applyPlotoptions(self):
        """Apply the current plotter/options"""
        if self.mode == 0:
            self.mplopts.applyOptions()
        elif self.mode == 1:
            self.mplopts3d.applyOptions()
        #elif self.mode == 2:
        #    self.factorplotter.applyOptions()
        self.plotCurrent()
        return

    def addFigure(self, parent, figure=None):
        """Add the tk figure canvas"""
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
        from matplotlib.figure import Figure
        if hasattr(self,'canvas'):
            self.canvas._tkcanvas.destroy()
        if figure == None:
            self.fig = f = Figure(figsize=(5,4), dpi=100)
        else:
            self.fig = f = figure
        a = f.add_subplot(111)
        canvas = FigureCanvasTkAgg(f, master=parent)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        canvas.get_tk_widget().configure(highlightcolor='gray75',
                                       highlightbackground='gray75')
        toolbar = NavigationToolbar2TkAgg(canvas, parent)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        self.ax = a
        self.canvas = canvas
        return

    def setFigure(self, f=None):
        from matplotlib.figure import Figure
        if f == None:
            self.fig = f = Figure(figsize=(5,4), dpi=100)
            self.ax = f.add_subplot(111)
        a = self.fig.get_size_inches()
        f.set_size_inches(a,forward=True)
        self.canvas.figure = f
        f.canvas = self.canvas
        self.canvas.draw()
        #mng = plt.get_current_fig_manager()
        self.canvas._tkcanvas.config('state')
        return

    def plotCurrent(self):
        """Plot current data"""
        if self.mode == 0:
            #self.setFigure()
            self.plot2D()
        elif self.mode == 1:
            self.plot3D()
        #elif self.mode == 2:
        #    self.factorplotter.data = self.data
        #    self.factorPlot()
        return

    def _checkNumeric(self, df):
        x = df.convert_objects()._get_numeric_data()
        if x.empty==True:
            return False

    def plot2D(self):
        """Draw method for current data. Relies on pandas plot functionality
           if possible. There is some temporary code here to make sure only the valid
           plot options are passed for each plot kind."""

        if not hasattr(self, 'data'):
            return
        #needs cleaning up
        valid = {'line': ['alpha', 'colormap', 'grid', 'legend', 'linestyle',
                          'linewidth', 'marker', 'subplots', 'rot', 'logx', 'logy',
                           'sharey', 'use_index', 'kind'],
                    'scatter': ['alpha', 'grid', 'linewidth', 'marker', 's', 'legend',
                            'colormap','logx', 'logy', 'use_index'],
                    'pie': ['colormap', 'legend', 'kind','subplots'],
                    'hexbin': ['alpha', 'colormap', 'grid', 'linewidth'],
                    'bootstrap': ['grid'],
                    'bar': ['alpha', 'colormap', 'grid', 'legend', 'linewidth', 'subplots',
                            'sharey', 'stacked', 'rot', 'kind'],
                    'barh': ['alpha', 'colormap', 'grid', 'legend', 'linewidth', 'subplots',
                            'stacked', 'rot', 'kind'],
                    'histogram': ['alpha', 'linewidth','grid','stacked','subplots','colormap',
                             'sharey','rot','bins', 'logx', 'logy'],
                    'heatmap': ['colormap','rot'],
                    'area': ['alpha','colormap','grid','linewidth','legend','stacked',
                             'kind','rot','logx'],
                    'density': ['alpha', 'colormap', 'grid', 'legend', 'linestyle',
                                 'linewidth', 'marker', 'subplots', 'rot', 'kind'],
                    'boxplot': ['alpha', 'linewidth', 'rot', 'grid'],
                    'scatter_matrix':['alpha', 'linewidth', 'marker', 'grid', 's'],
                    }

        from pandas.tools import plotting
        data = self.data
        if self._checkNumeric(data) == False:
            self.showWarning('no numeric data to plot')
            return
        kwds = self.mplopts.kwds
        kind = kwds['kind']
        by = kwds['by']
        by2 = kwds['by2']
        #valid kwd args for this plot type
        kwargs = dict((k, kwds[k]) for k in valid[kind])
        self.fig.clear()
        self.ax = ax = self.fig.add_subplot(111)

        if by != '':
            #groupby needs to be handled per group so we can add all the axes to
            #our figure correctly
            if by not in data.columns:
                self.showWarning('the grouping column must be in selected data')
                return
            if by2 != '' and by2 in data.columns:
                by = [by,by2]
            g = data.groupby(by)
            if len(g) >25:
                self.showWarning('too many groups to plot')
                return
            self.ax.set_visible(False)
            kwargs['subplots'] = False
            size = len(g)
            nrows = round(np.sqrt(size),0)
            ncols = np.ceil(size/nrows)
            i=1
            for n,df in g:
                ax = self.fig.add_subplot(nrows,ncols,i)
                kwargs['legend'] = False #remove axis legends
                d=df.drop(by,1) #remove grouping columns
                self._doplot(d, ax, kind, False, kwargs)
                ax.set_title(n)
                handles, labels = ax.get_legend_handles_labels()
                i+=1
            self.fig.legend(handles, labels, 'lower right')
            self.fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=.25)
            axs = self.fig.get_axes()
            #self.canvas.draw()
        else:
            axs = self._doplot(data, ax, kind, kwds['subplots'], kwargs)

        if type(axs) is np.ndarray:
            self.ax = axs.flat[0]
        elif type(axs) is list:
            self.ax = axs[0]
        self.fig.suptitle(kwds['title'])
        if kwds['xlabel'] != '':
            self.ax.set_xlabel(kwds['xlabel'])
        if kwds['ylabel'] != '':
            self.ax.set_ylabel(kwds['ylabel'])
        self.ax.xaxis.set_visible(kwds['showxlabels'])
        self.ax.yaxis.set_visible(kwds['showylabels'])
        try:
            self.fig.tight_layout()
        except:
            print ('tight_layout failed')
        self.canvas.draw()
        return

    def _doplot(self, data, ax, kind, subplots, kwargs):
        """Do actual plotting"""

        cols = data.columns
        rows = int(round(np.sqrt(len(data.columns)),0))
        if len(data.columns) == 1:
            kwargs['subplots'] = 0
        if kind == 'pie':
            kwargs['subplots'] = True
        if subplots == 0:
            layout=None
        else:
            layout=(rows,-1)
        if kind == 'bar':
            if len(data) > 50:
                ax.get_xaxis().set_visible(False)
            if len(data) > 500:
                print ('too many rows to plot')
                return
        if kind == 'scatter':
            axs = self.scatter(data, ax, **kwargs)
            #axs = data.plot(kind='scatter',ax=ax,**kwargs)
        elif kind == 'boxplot':
            axs = data.boxplot(ax=ax)
        elif kind == 'histogram':
            bins = int(kwargs['bins'])
            axs = data.plot(kind='hist',layout=layout, ax=ax, **kwargs)
        elif kind == 'heatmap':
            axs = self.heatmap(data, ax, kwargs)
        elif kind == 'bootstrap':
            axs = plotting.bootstrap_plot(data)
        elif kind == 'scatter_matrix':
            axs = pd.scatter_matrix(data, ax=ax, **kwargs)
        elif kind == 'hexbin':
            x = cols[0]
            y = cols[1]
            axs = data.plot(x,y,ax=ax,kind='hexbin',gridsize=20,**kwargs)
        else:
            axs = data.plot(ax=ax, layout=layout, **kwargs)
        return axs

    def scatter(self, df, ax, alpha=0.8, marker='o', **kwds):
        """A more custom scatter plot"""

        print (kwds)
        if len(df.columns)<2:
            return
        df = df._get_numeric_data()
        cols = df.columns
        x = df[cols[0]]
        s=1
        plots = len(cols)
        cmap = plt.cm.get_cmap(kwds['colormap'])
        if marker == '':
            marker = 'o'
        for i in range(s,plots):
            y = df[cols[i]]
            c = cmap(float(i)/(plots))
            if marker in ['x','+']:
                ec=c
            else:
                ec='black'
            ax.scatter(x, y, marker=marker, alpha=alpha, linewidth=kwds['linewidth'],
                       s=kwds['s'], color=c, edgecolor=ec)
            if kwds['logx'] == 1:
                ax.set_xscale('log')
            if kwds['logy'] == 1:
                ax.set_yscale('log')
        if kwds['grid'] == 1:
            ax.grid()
        if kwds['legend'] == 1:
            ax.legend(cols[1:])
        return ax

    def heatmap(self, df, ax, kwds):
        """Plot heatmap"""

        X = df._get_numeric_data()
        hm = ax.pcolor(X, cmap=kwds['colormap'])
        self.fig.colorbar(hm, ax=ax)
        ax.set_xticks(np.arange(0.5, len(X.columns)))
        ax.set_yticks(np.arange(0.5, len(X.index)))
        ax.set_xticklabels(X.columns, minor=False)
        ax.set_yticklabels(X.index, minor=False)
        return

    def plot3D(self):
        """3D plots"""
        if not hasattr(self, 'data'):
            return
        kwds = self.mplopts3d.kwds
        print (kwds)
        data = self.data
        self.fig.clear()
        ax = self.ax = Axes3D(self.fig)
        if kwds['kind'] == 'scatter':
            self.scatter3D(data, ax, kwds)
        elif kwds['kind'] == 'bar':
            self.bar3D(data, ax, kwds)
        elif kwds['kind'] == 'contour':
            X = data.values
            ax.contour(X[:,0], X[:,1], X[:,2])
        self.fig.suptitle(kwds['title'])
        self.ax.set_xlabel(kwds['xlabel'])
        self.ax.set_ylabel(kwds['ylabel'])
        self.ax.set_zlabel(kwds['zlabel'])
        self.canvas.draw()
        return

    def bar3D(self, data, ax, kwds):
        i=0
        plots=len(data.columns)
        cmap = plt.cm.get_cmap(kwds['colormap'])
        for c in data.columns:
            h = data[c]
            c = cmap(float(i)/(plots))
            ax.bar(data.index, h, zs=i, zdir='y', color=c)
            i+=1

    def scatter3D(self, data, ax, kwds):
        """3D scatter plot"""

        #print (kwds['by'])
        data = data._get_numeric_data()
        l = len(data.columns)
        if l<3: return
        X = data.values
        cmap = plt.cm.get_cmap(kwds['colormap'])
        x = X[:,0]
        for i in range(1,l-1):
            y = X[:,i]
            z = X[:,i+1]
            c = cmap(float(i)/(l))
            ax.scatter(x, y, z, color=c)
        return

    def factorPlot(self):
        """Seaborn facet grid plots"""

        import seaborn as sns
        if not hasattr(self, 'data'):
            return
        df = self.data
        labels = list(df.columns)
        dtypes = list(df.dtypes)
        x='id'
        print (labels)
        hue='label'
        col='var'
        row=None
        wrap=2
        kind='auto'
        aspect = 1.0

        print (df[:10])
        tm = pd.melt(df,id_vars=['label'],
                     var_name='var',value_name='x')
        print (tm[:10])

        '''plots = len(df[col].unique())
        wrap=int(wrap)
        if plots == 1 or wrap==1:
            row=col
            col=None
            wrap=None
        if hue == '':
            hue=None'''
        plt.clf()
        g = sns.factorplot('label','x',data=tm, hue=hue, row=row, col=col,
                                col_wrap=wrap, kind=kind,size=3, aspect=float(aspect),
                                legend_out=True,sharey=False,palette='Spectral')

        #rotateLabels(g)
        self.fig.clear()
        #need to reset the current figure
        self.setFigure(g.fig)
        return

    def updateData(self):
        """Update data widgets"""

        df = self.table.model.df
        self.mplopts.update(df)

        return

    def showWarning(self, s='plot error'):
        self.ax.clear()
        self.ax.text(.5, .5, s,transform=self.ax.transAxes,
                       horizontalalignment='center', color='blue', fontsize=16)
        self.canvas.draw()
        return

    def quit(self):
        #self.main.withdraw()
        self.table.pf = None
        self.main.destroy()
        return

class animator(Frame):

    def __init__(self, parent, plotframe):
        Frame.__init__(self, parent)
        self.main = Frame(self)
        self.main.pack(side=TOP, fill=BOTH, expand=1)
        self.plotframe = plotframe
        self.doGUI()
        return

    def doGUI(self):
        b = Button(self.main, text='animate', command=self.animate)
        b.pack(side=TOP)
        l = Label(self.main, text='arse')
        l.pack(side=TOP)
        return

    def animate(self):

        def run(i):
            line.set_ydata(np.sin(x+i/10.0))
            return line,
        fig = self.plotframe.fig
        data = self.plotframe.data
        ax = self.plotframe.ax
        ax.clear()
        x = np.arange(0, 2*np.pi, 0.01)
        line, = ax.plot(x, np.sin(x))
        ani = animation.FuncAnimation(fig, run, np.arange(1, 200),
                            blit=True, interval=10,
                            repeat=False)
        return

    def run(data, ax):
        """update the data"""
        t,y = data
        xdata.append(t)
        ydata.append(y)
        xmin, xmax = ax.get_xlim()
        if t >= xmax:
            ax.set_xlim(xmin, 2*xmax)
            ax.figure.canvas.draw()
        line.set_data(xdata, ydata)
        return line,

class MPLBaseOptions(object):
    """Class to provide a dialog for matplotlib options and returning
        the selected prefs"""

    markers = ['','o','.','^','v','>','<','s','+','x','p','d','h','*']
    linestyles = ['-','--','-.',':','steps']
    kinds = ['line', 'scatter', 'bar', 'barh', 'pie', 'histogram', 'boxplot',
             'heatmap', 'area', 'hexbin', 'scatter_matrix', 'density']

    def __init__(self, parent=None):
        """Setup variables"""

        self.parent = parent
        df = self.parent.table.model.df
        datacols = list(df.columns)
        datacols.insert(0,'')
        fonts = self.getFonts()
        grps = {'data':['bins','by','by2','use_index'],
                'styles':['font','colormap','alpha','grid'],
                'sizes':['fontsize','s','linewidth'],
                'formats':['kind','marker','linestyle','stacked','subplots'],
                'axes':['showxlabels','showylabels','sharex','sharey','logx','logy','rot'],
                'labels':['title','xlabel','ylabel','legend']}
        order = ['data','formats','sizes','axes','styles','labels']
        self.groups = OrderedDict(sorted(grps.items()))
        opts = self.opts = {'font':{'type':'combobox','default':'Arial','items':fonts},
                'fontsize':{'type':'scale','default':12,'range':(5,40),'interval':1,'label':'font size'},
                'marker':{'type':'combobox','default':'','items':self.markers},
                'linestyle':{'type':'combobox','default':'-','items':self.linestyles},
                's':{'type':'scale','default':30,'range':(5,500),'interval':10,'label':'marker size'},
                'grid':{'type':'checkbutton','default':0,'label':'show grid'},
                'logx':{'type':'checkbutton','default':0,'label':'log x'},
                'logy':{'type':'checkbutton','default':0,'label':'log y'},
                'rot':{'type':'entry','default':0, 'label':'ylabel rot'},
                'use_index':{'type':'checkbutton','default':1,'label':'use index'},
                'showxlabels':{'type':'checkbutton','default':1,'label':'x tick labels'},
                'showylabels':{'type':'checkbutton','default':1,'label':'y tick labels'},
                'sharex':{'type':'checkbutton','default':0,'label':'share x'},
                'sharey':{'type':'checkbutton','default':0,'label':'share y'},
                'legend':{'type':'checkbutton','default':1,'label':'legend'},
                'kind':{'type':'combobox','default':'line','items':self.kinds,'label':'kind'},
                'stacked':{'type':'checkbutton','default':0,'label':'stacked'},
                'linewidth':{'type':'scale','default':1,'range':(0,5),'interval':0.5,'label':'line width'},
                'alpha':{'type':'scale','default':0.7,'range':(0,1),'interval':0.1,'label':'alpha'},
                'title':{'type':'entry','default':'','width':20},
                'xlabel':{'type':'entry','default':'','width':20},
                'ylabel':{'type':'entry','default':'','width':20},
                'subplots':{'type':'checkbutton','default':0,'label':'multiple subplots'},
                'colormap':{'type':'combobox','default':'jet','items':colormaps},
                'bins':{'type':'entry','default':20,'width':10},
                'by':{'type':'combobox','items':datacols,'label':'group by','default':''},
                'by2':{'type':'combobox','items':datacols,'label':'group by 2','default':''},
                }
        return

    def applyOptions(self):
        """Set the options"""

        kwds = {}
        for i in self.opts:
            if self.opts[i]['type'] == 'listbox':
                items = self.widgets[i].curselection()
                kwds[i] = [self.widgets[i].get(j) for j in items]
                print (items, kwds[i])
            else:
                kwds[i] = self.tkvars[i].get()
        self.kwds = kwds
        size = kwds['fontsize']
        plt.rc("font", family=kwds['font'], size=size)
        plt.rc('legend', fontsize=size-1)
        return

    def apply(self):
        self.applyOptions()
        if self.callback != None:
            self.callback()
        return

    def showDialog(self, parent, callback=None):
        """Auto create tk vars, widgets for corresponding options and
           and return the frame"""

        dialog, self.tkvars, self.widgets = dialogFromOptions(parent, self.opts, self.groups)
        self.applyOptions()
        return dialog

    def getFonts(self):
        """Get the current list of system fonts"""

        import tkinter.font
        fonts = set(list(tkinter.font.families()))
        fonts = sorted(list(fonts))
        return fonts

    def update(self, df):
        """Update data widget(s)"""

        cols = list(df.columns)
        cols += ''
        self.widgets['by']['values'] = cols
        self.widgets['by2']['values'] = cols
        return

class MPL3DOptions(object):
    """Class to provide 3D matplotlib options"""

    kinds = ['scatter', 'bar', 'bar3d', 'surface', 'contour']

    def __init__(self, parent=None):
        """Setup variables"""

        self.parent = parent
        df = self.parent.table.model.df
        datacols = list(df.columns)
        datacols.insert(0,'')
        fonts = self.getFonts()
        self.groups = grps = {'styles':['font','fontsize','colormap','alpha'],
                            'formats':['kind','title','xlabel','ylabel','zlabel'],}
                            #'data':['by','subplots']}

        opts = self.opts = {'font':{'type':'combobox','default':'Arial','items':fonts},
                'fontsize':{'type':'scale','default':12,'range':(5,40),'interval':1,'label':'font size'},
                'kind':{'type':'combobox','default':'scatter','items':self.kinds,'label':'kind'},
                'alpha':{'type':'scale','default':0.8,'range':(0,1),'interval':0.1,'label':'alpha'},
                'title':{'type':'entry','default':'','width':25},
                'xlabel':{'type':'entry','default':'','width':25},
                'ylabel':{'type':'entry','default':'','width':25},
                'zlabel':{'type':'entry','default':'','width':25},
                #'subplots':{'type':'checkbutton','default':0,'label':'multiple subplots'},
                'colormap':{'type':'combobox','default':'jet','items': colormaps},
                #'by':{'type':'combobox','items':datacols,'label':'group by','default':''},
                 }

    def applyOptions(self):
        """Set the options"""

        kwds = {}
        for i in self.opts:
            kwds[i] = self.tkvars[i].get()
        self.kwds = kwds
        plt.rc("font", family=kwds['font'], size=kwds['fontsize'])
        return

    def showDialog(self, parent, callback=None):
        """Auto create tk vars, widgets for corresponding options and
           and return the frame"""

        dialog, self.tkvars, w = dialogFromOptions(parent, self.opts, self.groups)
        self.applyOptions()
        return dialog

    def getFonts(self):
        """Get the current list of system fonts"""

        import tkinter.font
        fonts = set(list(tkinter.font.families()))
        fonts = sorted(list(fonts))
        return fonts

class FactorPlotter(object):
    """Provides seaborn factor plots"""
    def __init__(self, data=None):
        """Setup variables"""

        self.data=data
        self.setDefaultStyle()
        self.groups = grps = {'formats':['style','despine','palette'],
                'factors':['kind','hue','x']}
        styles = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']
        kinds = ['auto','bar']
        palettes = ['Spectral','cubehelix','hls','hot','coolwarm','copper',
                    'winter','spring','summer','autumn','Greys','Blues','Reds',
                    'Set1','Accent']
        if self.data is not None:
            cols = self.data.columns

        self.opts = {'style': {'type':'combobox','default':'whitegrid','items':styles},
                     'despine': {'type':'checkbutton','default':0,'label':'despine'},
                     'palette': {'type':'combobox','default':'Spectral','items':palettes},
                     'kind': {'type':'combobox','default':'auto','items':kinds},
                     'x': {'type':'combobox','default':'auto','items':kinds},
                     'hue': {'type':'combobox','default':'auto','items':kinds},
                        }
        return

    def showDialog(self, parent, callback=None):
        """Auto create tk vars, widgets for corresponding options and
           and return the frame"""

        dialog, self.tkvars, w = dialogFromOptions(parent, self.opts, self.groups)
        #self.applyOptions()
        return dialog

    def applyOptions(self):
        """Set the options"""
        import seaborn as sns
        kwds = {}
        for i in self.opts:
            kwds[i] = self.tkvars[i].get()
        self.kwds = kwds
        sns.set_style(self.kwds['style'])
        if self.kwds['despine'] == 1:
            sns.despine()
        return

    def setDefaultStyle(self):
        import seaborn as sns
        sns.set_style("ticks", {'axes.facecolor': '#F7F7F7','legend.frameon': True})
        sns.set_context("paper", rc={'legend.fontsize':16,'xtick.labelsize':12,
                        'ytick.labelsize':12,'axes.labelsize':14,'axes.titlesize':16})
        return
