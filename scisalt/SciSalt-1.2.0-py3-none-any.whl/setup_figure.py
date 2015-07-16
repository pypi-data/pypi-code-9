import matplotlib.pyplot as plt
from matplotlib import gridspec


def setup_figure(gridspec_x=1, gridspec_y=1):
    fig = plt.figure()
    gs = gridspec.GridSpec(gridspec_x, gridspec_y)

    return fig, gs
