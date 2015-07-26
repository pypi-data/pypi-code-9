from IPython.display import display
from IPython.display import Math
from IPython.html import widgets
from dautil import ts
import matplotlib as mpl


def create_month_widget(month, *args, **kwargs):
    return widgets.Dropdown(options=ts.short_months(),
                            selected_label=month, *args, **kwargs)


def set_rc(rc_params={}):
    for k, v in rc_params.items():
        mpl.rcParams[k] = v


def create_rc_widget():
    box = widgets.VBox()
    axes_linewidth = create_linewidth_slider(0)
    axes_linewidth.description = 'axes_linewidth'

    grid_linewidth = create_linewidth_slider(2)
    grid_linewidth.description = 'grid_linewidth'

    text = widgets.HTML()
    box.children = (text, axes_linewidth, grid_linewidth)
    box.description = text

    box.value = {'axes.linewidth': axes_linewidth.value, 'grid.linewidth':
                 grid_linewidth.value}

    def update_axes_linewidth(name, value):
        box.value['axes.linewidth'] = value

    def update_grid_linewidth(name, value):
        box.value['grid.linewidth'] = value

    axes_linewidth.on_trait_change(update_axes_linewidth, 'value')
    grid_linewidth.on_trait_change(update_grid_linewidth, 'value')

    return box


def create_linewidth_slider(value, *args, **kwargs):
    return widgets.IntSlider(min=0, max=9, value=value, *args, **kwargs)


class LatexRenderer():
    def __init__(self, chapter=None, start=1):
        self.chapter = chapter
        self.curr = start

    # DIY numbering because Python doesn't
    # support numbering
    def number_equation(self):
        number = '('

        if self.chapter:
            number += str(self.chapter) + '.'

        number += str(self.curr) + ')\hspace{1cm}'

        return number

    def render(self, equation):
        number = self.number_equation()
        display(Math(r'%s' % (number + equation)))
        self.curr += 1
