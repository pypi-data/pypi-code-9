# -*- coding: utf-8 -*-
"""Functions to create graphs for ploting distributions of two variables at the same time.

TODO: Instead of calling plot for each point, we should use directly plt.scatter function and then get the points and add the annotations.
"""

import matplotlib.pyplot as plt


def drawTipBox(x, y, text, color, ax, alpha=0.9,):
    """ Adds a tootip box with text in he point on the ax specified with the color and alpha parameters. """

    # Containing box parameters
    bbox_props = dict(
        boxstyle="round,pad=0.80",
        fc=color,
        ec='none',
        alpha=alpha
    )

    # Arrow parameters (bellow the box)
    arrrow_props = dict(
        arrowstyle="wedge,tail_width=2.",
        fc=color,
        ec="none",
        patchA=None,
        relpos=(0.5, .5),
    )

    # Draw the box on the ax
    ann = ax.annotate(
        text,
        xy=(x, y),
        xycoords='data',
        xytext=(5, 35),
        textcoords='offset points',
        size=12,
        va="bottom",
        bbox = bbox_props,
        arrowprops = arrrow_props
    )

    # Return the annotation
    return ann



def plot_mouse_over_scatter(x, y, tips, box_color=(0.95, 0.90, 1), c=None, marker='o', ax=None, **kwargs):
    """ Draw a scatter plot adding a tooltip to be show when the mouse is passes over the point.

    The function calls ``plt.plot(...)`` method to each point separatedly and adds a hidden (by default)
    annotation over it. The annotation visibility is changed to True when the point is hovered.

    Parameters
    ----------
    x : List
        List of x coordinates.
    y : List
        List of y coordinates.
    tips : List
        List of the strings that will be shown when the mouse is over the point.
    box_collor : Color
        RGB color of the box behind the text. Default is (0.95, 0.90, 1).
    c : TODO
        TODO
    marker : Any valid marker symbol used in matplotlib scatter plots.
        The marker symbol.
    ax ; Axes
        The ax where the scatter will be plotted. Default is None.
    **kwargs
        Key word args to be passed to ``plt.plot(...)`` function.

    """

    # Set the default color, if a color array is not given
    if c is None:
        c = len(x)*['blue']

    assert len(x) == len(y) == len(tips) == len(c)

    # Initialize list of points and annotations
    points_with_annotation = []

    # Get current ax
    if ax is None:
        ax = plt.gca()

    # For pair of point and tip
    for i, x, y, tip in zip(range(0, len(c)), x, y, tips):

        # Draw the point ( the comma after point "automatically extracts" the item from the list
        point, = ax.plot(x, y, marker, color=c[i], **kwargs)

        # Draw the annotation box
        annotation = drawTipBox(x, y, tip, box_color, ax=ax)

        # Disable the annotation visibility
        annotation.set_visible(False)

        # Store the point with its annotation in a list
        points_with_annotation.append([point, annotation])

    # Function to show/hide points with mouseover event (to be execute whenever the mouse is moved)
    def on_move(event):


        # For each point, annotation pair
        for point, annotation in points_with_annotation:

            # Determine whether it should be visible (when the space occupied by the point contains the coordinates of the mouseover event
            should_be_visible = (point.contains(event)[0] == True)

            # If the visibility of a point changed
            if should_be_visible != annotation.get_visible():

                # Show the point and redraw
                annotation.set_visible(should_be_visible)
                plt.draw()


    # Get current figure
    fig = plt.gcf()

    # Register the move event with the on_move function
    on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)

    plt.show()




