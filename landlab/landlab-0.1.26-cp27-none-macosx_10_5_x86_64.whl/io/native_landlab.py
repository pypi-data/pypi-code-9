#! /usr/bin/env python
"""
Read data from an ESRI ASCII file into a RasterModelGrid
"""

import os
import types
import re
from six.moves import cPickle
from landlab import ModelGrid
import numpy as np


def save_grid(grid, path, clobber=False):
    """Save a grid and fields to a Landlab "native" format.

    This method uses cPickle to save a grid as a cPickle file.
    All fields will be saved, along with the grid.

    The recommended suffix for the save file is '.grid'. This will
    be added to your save if you don't include it.

    Caution: Pickling can be slow, and can produce very large files.
    Caution 2: Future updates to Landlab could potentially render old
    saves unloadable.

    Parameters
    ----------
    grid : object of subclass ModelGrid
        Grid object to save
    path : str
        Path to output file, either without suffix, or '.grid'
    clobber : bool (default False)
        Set to True to allow overwrites of existing files

    Examples
    --------
    >>> from landlab import RasterModelGrid
    >>> from landlab.io.native_landlab import save_grid
    >>> import os
    >>> grid_out = RasterModelGrid(4,5,2.)
    >>> save_grid(grid_out, 'testsavedgrid.grid', clobber=True)
    >>> os.remove('testsavedgrid.grid') #to remove traces of this test
    """
    if os.path.exists(path) and not clobber:
        raise ValueError('file exists')
        
    #test it's a grid
    assert issubclass(type(grid), ModelGrid)
        
    (base, ext) = os.path.splitext(path)
    if ext != '.grid':
        ext = ext+'.grid'
    path = base+ext

    with open(path, 'wb') as fp:
        cPickle.dump(grid, fp)


def load_grid(path):
    """Load a grid and its fields from a Landlab "native" format.
    
    This method uses cPickle to load a saved grid.
    It assumes you saved using vmg.save() or save_grid, i.e., that the
    pickle file is a .grid file.
    
    Caution: Pickling can be slow, and can produce very large files.
    Caution 2: Future updates to Landlab could potentially render old
    saves unloadable.

    Parameters
    ----------
    path : str
        Path to output file, either without suffix, or '.grid'

    Examples
    --------
    >>> from landlab import VoronoiDelaunayGrid
    >>> from landlab.io.native_landlab import load_grid, save_grid
    >>> import numpy as np
    >>> import os
    >>> x = np.random.rand(20)
    >>> y = np.random.rand(20)
    >>> grid_out = VoronoiDelaunayGrid(x, y)
    >>> save_grid(grid_out, 'testsavedgrid.grid', clobber=True)
    >>> grid_in = load_grid('testsavedgrid.grid')
    >>> os.remove('testsavedgrid.grid') #to remove traces of this test
    """
    
    (base, ext) = os.path.splitext(path)
    if ext != '.grid':
        ext = ext+'.grid'
    path = base+ext
    with open(path, 'rb') as fp:
        loaded_grid = cPickle.load(fp)
    assert issubclass(type(loaded_grid), ModelGrid)
    return loaded_grid

