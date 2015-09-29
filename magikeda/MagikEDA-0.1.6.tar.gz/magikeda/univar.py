# -*- coding: utf-8 -*-
"""Functions to create graphs for ploting distributions of single variables.
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

from matplotlib.gridspec import GridSpec


def _is_numeric(series):
    """ Determine if the pandas.core.series.Series is numeric """
    return series.dtype == 'int' or series.dtype == 'float'

def _is_categorical(series):
    """ Determine if the pandas.core.series.Series is categorical """
    return str(series.dtype) == 'object' or str(series.dtype) == 'category'

def _get_percentage_of_categorical(series):
    """ Return a Pandas series with the percents of each category, indexed by the categries names """
    counts = series.value_counts()
    porcentagens = 100 * (counts / sum(counts))
    return porcentagens


def plot_bar_chart(data, cmap='Accent', color=None, xlabel='', ylabel='', title='', width=0.9, xticks_rotation=0, series_legends=None, ax=None):
    """Plot a barplot showing the distribution of a categorical variable (for one or multiple series of data).

    It's similar to ``series.value_counts().plot(kind='bar')`` but can also be used with multiple series at the same time (a lista of series in data).

    Parameters
    ----------
    data : List
        Pandas series (with categorical data) or list of series. For multiple series, each categories are grouped together.
    cmap : str
        Colormap to use for determining each category color. Default is 'Accent'.
    color : Color
        color to use in the graph (overrides colormap colors). Default is None, which means not to override colormap colors.
    xlabel : str
        Label of the x axis.
    ylabel : str
        Label of the x axis.
    title : str
        Figure title.
    width : float
        Width of each bar. Default is 0.9
    xticks_rotation : float
        Degrees to rotate x labels.
    series_legends : List[str]
        Lgends to identify each series.
    legend : bool
        Whether to show or not the legend box.
    ax : Axes
        Axes in which to plot the graph

    Returns
    -------
    ax : Axes
        Axes where the figure has been plotted.

    """

    # In the case a unique series is passed as parameters, wrap it in a list
    if not isinstance(data, list):
        data = [data]
        
    # Determine series type (pandas can represent categorical data with at least three different classes!)
    data_type = str(data[0].dtype)
  
    # If the Series is of "objects" (usually strings)
    if data_type == 'object':
        
        # Get list of different strings
        categorias = np.unique(data)
        
    # If it is a series create by pd.Series([...], dtype='category') or equivalent (e.g. pd.Series(pd.Categorical([...], [...])) )
    elif data_type == 'category':             
        
        # Get list of categories
        categorias = data[0].cat.categories # We assume here that the first series has all categories (BUG: it can be wrong!!!)
        
    else:
        raise Exception('Invalid data type %s' % data[0].dtype )
    
    # Number of different categories
    num_of_categories = len(categorias)
    
    # Number of series
    num_de_series = len(data)
    
    # Colormap to use in the graph
    colors = plt.cm.get_cmap(cmap, num_de_series)     
    
    # Position of each category
    x_locations = np.arange(num_of_categories) * num_de_series
    
    # Create figure
    if ax == None:
        fig, ax = plt.subplots()
    
    # Create series names, if not provided    
    if series_legends == None:    
        series_legends = ['Series %i' % i for i in range(1, num_de_series + 1)]    
    
    # For each series
    for idx, series in enumerate(data):
               
        # Compute the porcentage of each category
        porcentagens = _get_percentage_of_categorical(series)      
        porcentagens = porcentagens[categorias] # Assure that percentages will be returned in the same order as the legend
        
        # Determine color to use in this series
        series_color = color if color != None else colors(idx)      
        
        # Plot bars
        ax.bar(x_locations + idx*width, porcentagens, width, color=series_color, label=series_legends[idx])

    # Plot title and axis labels
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)    
            
    # If there is more than one series
    if num_de_series > 1:
        
        # Show legend
        ax.legend(loc='best')
        
        # Draw categories names
        #...        
        
    # If there is just one series
    else:
        
        # Draw categories names
        ax.set_xticks(x_locations + width/2)
        categorias = [cat.decode('utf8') for cat in categorias] # Convert categires names to utf8 (matplotlib doesn't non ascii chars)
        ax.set_xticklabels(categorias, rotation=xticks_rotation)
    
    
    # Add some small gap before the first and after the last category
    ax.set_xlim(min(x_locations) - width/9, max(x_locations) + width*num_de_series + width/9)

    # Return the axes in which the graph was plotted
    return ax


def plot_dataframe_profile(data_frame, include_cols=None, exclude_cols=None, shape = None, hspace=0.4, wspace=0.2, default_xticks_rotation=0, xticks_rotation={}, default_color='blue', colors={}, bins=30, title='', titles={}, default_ylabel='', ylabels={}, default_xlabel='', xlabels={}):
    """Plot a grid of subplots in which each subplot shows the distribution of a variable of the data frame.

    For numerical variables a histogram is shown. For categorical, a barplot whose bars lengths are proportional
    to the percentage of each category in the column. The subplots are drawn in the default column order in the
    dataframe, or in the order specified in include_cols.
    
    Parameters
    ----------
    data_frame : Dataframe
        The Pandas data frame whose columns will be plotted.
    include_cols : List
        A list with the column names that should be included in the plot. Default is None, which means all columns.
        If this parameter is used, just the columns specified are included, in the given order.
    remove_cols : List
        A list with the column names that should not be included in the plot. Columns listed here will be removed
        even if included in the include_cols list.
    shape : tuple
        A (rows, columns) tuples indicating the shape of the grid. Default is to use the square root of the number of variables
        as the number of columns, and as many rows as necessary to show all variables.
    hspace : float
        Vertical space between subplots.
    wspace : float
        Horizontal space between subplots.
    default_xticks_rotation : float
        Default rotation in degrees of the category names in bar graphs.
    xticks_rotation : dict
        Dictionary associating column names to xtick label orientation (in degrees).
    default_color : str
        Default color name for all subplots.
    colors : dict
        Dictionary associating column names to colors (override defaults color).
    title : str
        General title to use above all subplots.
    titles : dict
        Dictionary associating column names to titles to use in each subplot. If a value is not specified for a
        column, the colum name is used as title.
    default_ylabel : str
        Default lable to use in the y axis.
    ylabels : dict
        Dictionary associating columnnames to y labels to use in each subplot. If a value is not specified for a
        column, the ``default_ylabel`` is used.
    default_xlabel : str
        Default lable to use in the y axis.
    xlabels : dict
        Dictionary associating columnnames to y labels to use in each subplot. If a value is not specified for a
        column, the ``default_ylabel`` is used.
                
                
    Returns
    -------
    gs : GridSpec
        Return the GridSpec created with the subplots.

    """
    
    # Keep just specified columns, if it is the case
    if include_cols != None:
        #data_frame = data_frame[include_cols]
        columns_kept = include_cols
    else:
        columns_kept = data_frame.columns
        
    # Remove cols specified
    if exclude_cols != None:
        columns_kept = [x for x in columns_kept if x not in exclude_cols]
            
    # Get number of columns
    num_of_columns = len(columns_kept)
    
    # Get the number of rows and cols
    if shape != None:
        rows, cols = shape  # Unpack tuple passed as parameter
    else:
        
        # Number of columns in the plot (as the square root (rounded) of the number of variables)
        cols = int(math.ceil(math.sqrt(num_of_columns)))             
        
        # Number or rows in the plot (the necessary to put all variables)
        rows = int(math.ceil(num_of_columns / float(cols)))
    
    # Create a grid with rows x cols subplots
    gs = GridSpec(rows, cols, hspace=hspace, wspace=wspace)        
    
    # For each column
    for col_idx, column_name in enumerate(columns_kept):        
        
        # Create the subplot
        ax = plt.subplot(gs[col_idx])        
        
        # Determine the rotation of xticks for this plot                
        rotation = xticks_rotation[column_name] if column_name in xticks_rotation else default_xticks_rotation            

        # Determine the color
        subplot_color = colors[column_name] if column_name in colors else default_color
        
        # Determine subplot title
        subplot_title = titles[column_name] if column_name in titles else column_name.decode('utf8')    
        
        # Is it is categorical
        if _is_categorical(data_frame[column_name]):                      
            
            # Plot barplot
            plot_bar_chart(data_frame[column_name], ax=ax, title=subplot_title, xticks_rotation=rotation, color=subplot_color)         
        
        # If it is numeric
        if _is_numeric(data_frame[column_name]):
            
            # Calculate the weiths used to transform data in percents
            weigths = (np.zeros_like(data_frame[column_name]) + 100.) / len(data_frame[column_name])
            
            # Plot histogram
            ax.hist(data_frame[column_name], weights=weigths, color=subplot_color, bins=bins)
            ax.set_title(subplot_title)
            ax.grid()
            
        # Set the y label
        ylabel = ylabels[column_name] if column_name in ylabels else default_ylabel
        ax.set_ylabel(ylabel)
        
        # Set the x Label
        xlabel = xlabels[column_name] if column_name in xlabels else default_xlabel
        ax.set_xlabel(xlabel)        
            
    # Set the general title
    plt.suptitle(title)
            
    # Return the GridSpec with subplots
    return gs


def add_extra_xaxis(fig, x, labels, padding=35):
    """Add a x axis bellow the figure (indeed bellow the ax returned by ``fig.gca())`` having the labels
    in the x positions.

    The axis is added by first adding an entire new axes and the hiding all
    parts, except the xaxis.

    Parameters
    ----------
    fig : Figure
        The figure where to add the xaxis.
    x : List
        List of numbers specifying the x positions.
    labels : List
        List of strings specifying the labels to place in the x positions.
    padding : int
        How much space should be added between the figure and the new x axis bellow it.

    Returns
    -------
    new_ax : Axes
        Return the axes added to the image (where the x axis was plotted).

    """

    # Add some space bellow the figure
    fig.subplots_adjust(bottom=0.2)

    # Get current ax
    ax = fig.gca()

    # Add a new ax to the figure
    new_ax = fig.add_axes(ax.get_position())

    # Hide the the plot area and the yaxis
    new_ax.patch.set_visible(False)
    new_ax.yaxis.set_visible(False)

    # Hide spines (unless the boottom one)
    for spinename, spine in new_ax.spines.iteritems():
        if spinename != 'bottom':
            spine.set_visible(False)

    # Set the ....
    new_ax.spines['bottom'].set_position(('outward', padding))

    # Change tick labels
    plt.xticks([0] + x, [''] + labels) # the [0] and [''] stuff is to add an empty lable in the first position

    return new_ax

if __name__=='__main__':
    
    pass