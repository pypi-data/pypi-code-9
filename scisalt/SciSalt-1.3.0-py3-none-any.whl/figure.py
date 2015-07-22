from matplotlib.pyplot import figure as _figure


def figure(title=None, **kwargs):
    fig = _figure(**kwargs)
    if title is not None:
        fig.canvas.set_window_title(title)
    return fig
