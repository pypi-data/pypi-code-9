import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import matplotlib.pyplot as _plt
    from matplotlib import gridspec as _gridspec


def setup_figure(rows=1, cols=1, figsize=(8, 6)):
    """
    .. versionchanged:: 1.1.2
       Changed *gridspec_x* to *rows*, *gridspec_y* to *cols*, added *figsize* control.

    Sets up a figure of size *figsize* with a number of rows (*rows*) and columns (*cols*).

    Returns :code:`fig, gs`:

    * *fig*: :class:`matplotlib.figure.Figure` instance
    * *gs*: :class:`matplotlib.gridspec.GridSpec` instance with *gridspec_x* rows and *gridspec_y* columns
    """
    fig = _plt.figure(figsize=figsize)
    gs = _gridspec.GridSpec(rows, cols)

    return fig, gs
