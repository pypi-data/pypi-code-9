import os
import matplotlib.pyplot as plt
import numpy as np

def readfile(filename, col_key_line=0, comment_char='#', string_column=None,
             string_length=16, only_keys=None):
    '''
    read a file as a np array, uses the comment char and col_key_line
    to get the name of the columns.
    
    Parameters
    ----------
    filename : str
        path to file
    
    col_key_line : int
        line number to find the column names (default 0)
    
    comment_char : str
        character to ignore as a comment (default #)
    
    string_column : int or list
        column numbers that should be read as strings (defult None)
    
    string_length : int
        maximum length of column string (default 16)
    
    only_keys : list
        column names to read (default all)
        
    Returns
    -------
    np.array from np.genfromtxt
    '''
    if col_key_line == 0:
        with open(filename, 'r') as f:
            line = f.readline()
        col_keys = line.replace(comment_char, '').strip().translate(None, '/[]-').split()
    else:
        with open(filename, 'r') as f:
            lines = f.readlines()
        col_keys = lines[col_key_line].replace(comment_char, '').strip().translate(None, '/[]').split()
    usecols = range(len(col_keys))

    if only_keys is not None:
        only_keys = [o for o in only_keys if o in col_keys]
        usecols = list(np.sort([col_keys.index(i) for i in only_keys]))
        col_keys = list(np.array(col_keys)[usecols])

    dtype = [(c, '<f8') for c in col_keys]
    if string_column is not None:
        if type(string_column) is list:
            for s in string_column:
                dtype[s] = (col_keys[s], '|S%i' % string_length)
        else:
            dtype[string_column] = (col_keys[string_column], '|S%i' % string_length)
    data = np.genfromtxt(filename, dtype=dtype, invalid_raise=False,
                         usecols=usecols, skip_header=col_key_line + 1)
    return data


class StarPop(object):
    """
    a class to read trilegal catalog
    """
    def __init__(self, trilegal_catalog):
        """
        Load data from a trilegal catalog
        Calls either astropy.table.Table.read or readfile
        adds self.base, self.name: file location and file name
        adds self.key_dict: a dictionary of column keys and their indices
        adds self.data: a np.array of the trilegal catalog
        """
        self.base, self.name = os.path.split(trilegal_catalog)
        
        try:
            from astropy.table import Table
            data = Table.read(trilegal_catalog, format='ascii.commented_header',
                              guess=False)
        except ImportError:
            data = readfile(trilegal_catalog)
        self.key_dict = dict(zip(list(data.dtype.names),
                                 range(len(list(data.dtype.names)))))
        self.data = data

    def split_column(self, colstr):
        """
        Useful way to deal with mags and colors.
        if there is a "-" in colstr, return the subtracted data values
        if not, return the data values of colstr
        """
        if '-' in colstr:
            col1, col2 = colstr.split('-')
            data = self.data[col1] - self.data[col2]
        else:
            data = self.data[colstr]
        return data


def color_by_arg(starpop, xdata, ydata, coldata, bins=None, cmap=None, ax=None,
                 fig=None, labelfmt='$%.3f$', xlim=None, ylim=None, clim=None,
                 slice_inds=None, skw={}):
    """
    Parameters
    ----------
    starpop : StarPop instance
        population to plot

    xdata, ydata, coldata : array or str
        xdata array or column name of starpop.data
        if column name, will add xlabel, ylabel, or colorbar label.

    cmap : mpl colormap instance
        colormap to use

    ax : plt.Axes instance

    bins : int or array
        make the color bar discrete with specified bin numbers

    labelfmt : str, optional (default='$%.3f$')
        colorbar label format

    xlim, ylim : tuples
        if set, adjust the limits on the x and y axes

    slice_inds : list or array
        slice the data
    
    Returns
    -------
    ax : plt.Axes instance
    """
    if type(starpop) is str:
        starpop = StarPop(starpop)

    def latexify(string):
        return r'${}$'.format(string.replace('_', '\_'))
    
    ax = ax or plt.gca()

    if type(xdata) is str:
        ax.set_xlabel(latexify(xdata))
        xdata = starpop.split_column(xdata)

    if type(ydata) is str:
        ax.set_ylabel(latexify(ydata))
        ydata = starpop.split_column(ydata)

    collabel = None
    if type(coldata) is str:
        collabel = latexify(coldata)
        coldata = starpop.split_column(coldata)

    if slice_inds is not None:
        xdata = xdata[slice_inds]
        ydata = ydata[slice_inds]
        coldata = coldata[slice_inds]
         
    if bins is not None:
        if cmap is None:
            cmap = plt.get_cmap('Spectral', bins)
        else:
            cmap = plt.get_cmap(cmap, bins)
        cmap.set_under('gray')
        cmap.set_over('gray')
    else:
        if cmap is not None:
            cmap = plt.get_cmap(cmap)
        cmap = cmap or plt.cm.Spectral
    
    l = ax.scatter(xdata, ydata, c=coldata, marker='o', s=15,
                   edgecolors='none', cmap=cmap, **skw)

    c = plt.colorbar(l, ax=ax)
    if collabel is not None:
        c.set_label(collabel)
  
    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    if clim is not None:
        l.set_clim(clim)
    return ax

