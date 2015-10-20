import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    from matplotlib.pyplot import figure as _figure


def figure(title=None, **kwargs):
    """
    Creates a figure with *\*\*kwargs* with a window title *title*.

    Returns class :class:`matplotlib.figure.Figure`.
    """
    fig = _figure(**kwargs)
    if title is not None:
        fig.canvas.set_window_title(title)
    return fig
